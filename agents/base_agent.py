from abc import ABC, abstractmethod
from typing import Dict, List, Any
from pydantic import BaseModel
from dashscope import Generation
from core.coordinator import Coordinator
import asyncio
import logging
import sys
import traceback

class AgentState(BaseModel):
    """Base state model for all agents"""
    name: str
    role: str
    current_task: str = ""
    memory: List[Dict[str, Any]] = []
    status: str = "idle"

class BaseAgent(ABC):
    def __init__(self, name: str, role: str, coordinator: Coordinator):
        self.state = AgentState(name=name, role=role)
        self.coordinator = coordinator
        self.conversation_id = None
        self.logger = logging.getLogger(__name__)

    @abstractmethod
    async def process_message(self, message: str) -> str:
        """Process incoming messages and generate responses"""
        pass

    def update_state(self, **kwargs):
        """Update agent state with new information"""
        for key, value in kwargs.items():
            if hasattr(self.state, key):
                setattr(self.state, key, value)
        self.coordinator.update_agent_state(self.state.name, self.state.dict())

    def add_to_memory(self, item: Dict[str, Any]):
        """Add new information to agent's memory"""
        self.state.memory.append(item)
        self.coordinator.update_agent_state(self.state.name, self.state.dict())

    def get_memory(self) -> List[Dict[str, Any]]:
        """Retrieve agent's memory"""
        return self.state.memory

    def clear_memory(self):
        """Clear agent's memory"""
        self.state.memory = []
        self.coordinator.update_agent_state(self.state.name, self.state.dict())

    async def generate_response(self, prompt: str, context: str = "") -> str:
        """Generate response using Qwen model"""
        try:
            # 在一个单独的线程中运行同步的SDK调用，以避免阻塞事件循环
            response = await asyncio.to_thread(
                Generation.call,
                model='qwen-turbo',
                prompt=f"{context}\n\n{prompt}",
                temperature=0.7,
                max_tokens=2000
            )
            # 检查API返回的响应是否成功
            if response.status_code == 200:
                return response.output.text
            else:
                # 如果API返回错误，则将其作为异常信息处理
                error_message = (f"DashScope API Error: Status {response.status_code}, "
                                 f"Code: {response.code}, Message: {response.message}")
                raise Exception(error_message)
        except Exception as e:
            # 捕获所有异常，并将详细信息作为字符串返回，用于调试
            error_info = f"Caught Exception: {str(e)}\n{traceback.format_exc()}"
            print(error_info, file=sys.stderr)
            return "An error occurred while generating the response. Please check the server logs for details."

    def set_conversation(self, conversation_id: str):
        """Set the current conversation ID"""
        self.conversation_id = conversation_id

    def get_conversation_context(self, max_messages: int = 10) -> str:
        """Get conversation context"""
        if not self.conversation_id:
            return ""
        return self.coordinator.get_context(self.conversation_id, max_messages) 