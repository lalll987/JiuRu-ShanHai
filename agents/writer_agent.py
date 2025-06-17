from typing import Dict, List, Any
from .base_agent import BaseAgent
from dashscope import Generation

class WriterAgent(BaseAgent):
    def __init__(self, name: str = "Writer Agent", coordinator=None):
        super().__init__(name=name, role="Academic Paper Writer", coordinator=coordinator)
        self.writing_style = {
            "academic_level": "high",
            "clarity": "high",
            "coherence": "high",
            "formality": "high"
        }
        self.paper_sections = {
            "introduction": "",
            "literature_review": "",
            "methodology": "",
            "results": "",
            "discussion": "",
            "conclusion": ""
        }
        self.writing_history: List[Dict[str, Any]] = []

    async def process_message(self, message: str) -> str:
        """Process incoming messages and generate responses"""
        try:
            context = self.get_conversation_context()
            
            system_prompt = f"""你是一位专注于学术论文写作的专家。
            你的主要职责是：
            1. 整合研究框架、数据和研究结果
            2. 采用层次化写作方法
            3. 确保论文的精准性和清晰度
            4. 保持学术写作的规范性和专业性
            
            当前论文状态：
            {self.paper_sections}
            
            写作风格要求：
            {self.writing_style}
            
            请基于以下上下文提供专业的写作建议：
            {context}
            """
            
            response = await self.generate_response(message, system_prompt)
            
            writing_record = {
                "type": "writing_feedback",
                "content": response,
                "timestamp": "current_time"
            }
            self.writing_history.append(writing_record)
            
            return response
        except Exception as e:
            print(f"Error in Writer agent: {e}")
            return f"Error generating response: {str(e)}"

    def update_section(self, section: str, content: str):
        """更新论文特定部分的内容"""
        if section in self.paper_sections:
            self.paper_sections[section] = content
            self.writing_history.append({
                "type": "section_update",
                "section": section,
                "content": content,
                "timestamp": "current_time"
            })

    def get_paper_status(self) -> Dict[str, Any]:
        """获取当前论文状态"""
        return {
            "sections": self.paper_sections,
            "writing_style": self.writing_style
        }

    def get_writing_history(self) -> List[Dict[str, Any]]:
        """获取所有写作历史"""
        return self.writing_history 