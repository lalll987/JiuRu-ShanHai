from typing import Dict, List, Any
from .base_agent import BaseAgent
from dashscope import Generation

class DrAgent(BaseAgent):
    def __init__(self, name: str = "Dr Agent", coordinator=None):
        super().__init__(name=name, role="Research Status Analyst", coordinator=coordinator)
        self.expertise_areas = [
            "Literature Review",
            "Research Gap Analysis",
            "Methodology Assessment",
            "Theoretical Contribution"
        ]
        self.analysis_history: List[Dict[str, Any]] = []

    async def process_message(self, message: str) -> str:
        """Process incoming messages and generate responses"""
        try:
            context = self.get_conversation_context()
            
            system_prompt = f"""你是一位专注于研究现状分析的博士研究员。
            你的专长领域包括：{', '.join(self.expertise_areas)}
            你的主要职责是：
            1. 分析当前研究主题的研究现状
            2. 识别研究空白和机会
            3. 评估研究方法的适当性
            4. 提供理论贡献建议
            
            请基于以下上下文提供专业的分析和建议：
            {context}
            """
            
            response = await self.generate_response(message, system_prompt)
            
            analysis = {
                "type": "research_analysis",
                "content": response,
                "timestamp": "current_time"
            }
            self.analysis_history.append(analysis)
            
            return response
        except Exception as e:
            print(f"Error in Dr agent: {e}")
            return f"Error generating response: {str(e)}"

    def analyze_research_status(self, topic: str) -> Dict[str, Any]:
        """分析研究主题的现状"""
        analysis = {
            "current_status": "",
            "research_gaps": [],
            "opportunities": [],
            "methodology_suggestions": [],
            "theoretical_contributions": []
        }
        self.analysis_history.append({
            "type": "status_analysis",
            "topic": topic,
            "content": analysis,
            "timestamp": "current_time"
        })
        return analysis

    def get_analysis_history(self) -> List[Dict[str, Any]]:
        """获取所有分析历史"""
        return self.analysis_history 