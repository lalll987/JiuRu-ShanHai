from typing import Dict, List, Any
import json
import redis
from datetime import datetime

class Coordinator:
    def __init__(self):
        # 初始化Redis连接
        self.redis_client = redis.Redis(host='localhost', port=6379, db=0)
        self.conversation_key_prefix = "conversation:"
        self.max_history_length = 1000

    def store_conversation(self, conversation_id: str, message: Dict[str, Any]):
        """存储对话历史"""
        key = f"{self.conversation_key_prefix}{conversation_id}"
        message['timestamp'] = datetime.now().isoformat()
        self.redis_client.rpush(key, json.dumps(message))
        # 保持历史记录在限定长度内
        self.redis_client.ltrim(key, -self.max_history_length, -1)

    def get_conversation_history(self, conversation_id: str) -> List[Dict[str, Any]]:
        """获取对话历史"""
        key = f"{self.conversation_key_prefix}{conversation_id}"
        history = self.redis_client.lrange(key, 0, -1)
        return [json.loads(msg) for msg in history]

    def get_context(self, conversation_id: str, max_messages: int = 10) -> str:
        """获取最近的对话上下文"""
        history = self.get_conversation_history(conversation_id)
        recent_messages = history[-max_messages:]
        return "\n".join([f"{msg['role']}: {msg['content']}" for msg in recent_messages])

    def broadcast_message(self, sender: str, message: str, conversation_id: str):
        """广播消息给所有相关智能体"""
        message_data = {
            "sender": sender,
            "content": message,
            "timestamp": datetime.now().isoformat()
        }
        self.store_conversation(conversation_id, message_data)
        return message_data

    def get_agent_state(self, agent_id: str) -> Dict[str, Any]:
        """获取智能体状态"""
        key = f"agent_state:{agent_id}"
        state = self.redis_client.get(key)
        return json.loads(state) if state else {}

    def update_agent_state(self, agent_id: str, state: Dict[str, Any]):
        """更新智能体状态"""
        key = f"agent_state:{agent_id}"
        self.redis_client.set(key, json.dumps(state))

    def create_conversation(self, topic: str) -> str:
        """创建新的对话"""
        conversation_id = f"conv_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        initial_message = {
            "role": "system",
            "content": f"New conversation started with topic: {topic}",
            "timestamp": datetime.now().isoformat()
        }
        self.store_conversation(conversation_id, initial_message)
        return conversation_id 