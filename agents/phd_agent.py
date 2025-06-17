from typing import Dict, List, Any
from .base_agent import BaseAgent
from dashscope import Generation

class PhDAgent(BaseAgent):
    def __init__(self, name: str = "PhD Agent", coordinator=None):
        super().__init__(name=name, role="PhD Research Framework Developer", coordinator=coordinator)
        self.research_framework = {
            "research_question": "",
            "theoretical_framework": "",
            "methodology": "",
            "expected_contributions": "",
            "revision_history": []
        }
        self.feedback_history: List[Dict[str, Any]] = []

    async def process_message(self, message: str) -> str:
        """Process incoming messages and generate responses"""
        try:
            context = self.get_conversation_context()
            
            system_prompt = f"""你是一位专注于研究框架开发的博士研究员。
            你的主要职责是：
            1. 基于多轮思维链分析研究主题
            2. 整合Dr Agents的反馈
            3. 修正和完善研究框架
            4. 确保研究框架的逻辑性和创新性
            
            当前研究框架状态：
            {self.research_framework}
            
            请基于以下上下文提供专业的分析和建议：
            {context}
            """
            
            response = await self.generate_response(message, system_prompt)
            
            feedback = {
                "type": "framework_feedback",
                "content": response,
                "timestamp": "current_time"
            }
            self.feedback_history.append(feedback)
            
            return response
        except Exception as e:
            print(f"Error in PhD agent: {e}")
            return f"Error generating response: {str(e)}"

    def update_framework(self, section: str, content: str):
        """更新研究框架的特定部分"""
        if section in self.research_framework:
            self.research_framework[section] = content
            self.research_framework["revision_history"].append({
                "section": section,
                "content": content,
                "timestamp": "current_time"
            })

    def get_framework_status(self) -> Dict[str, Any]:
        """获取当前研究框架状态"""
        return self.research_framework

    def get_feedback_history(self) -> List[Dict[str, Any]]:
        """获取所有反馈历史"""
        return self.feedback_history 