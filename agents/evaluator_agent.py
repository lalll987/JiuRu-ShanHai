from typing import Dict, List, Any
from .base_agent import BaseAgent
from dashscope import Generation

class EvaluatorAgent(BaseAgent):
    def __init__(self, name: str = "Evaluator Agent", coordinator=None):
        super().__init__(name=name, role="Paper Quality Evaluator", coordinator=coordinator)
        self.evaluation_criteria = {
            "reliability": {
                "methodology": 0.0,
                "data_quality": 0.0,
                "analysis_rigor": 0.0,
                "reproducibility": 0.0
            },
            "innovation": {
                "theoretical_contribution": 0.0,
                "methodological_innovation": 0.0,
                "practical_implications": 0.0,
                "future_directions": 0.0
            },
            "clarity": {
                "writing_quality": 0.0,
                "structure": 0.0,
                "argumentation": 0.0,
                "presentation": 0.0
            }
        }
        self.evaluation_history: List[Dict[str, Any]] = []

    async def process_message(self, message: str) -> str:
        """Process incoming messages and generate responses"""
        try:
            context = self.get_conversation_context()
            
            system_prompt = f"""你是一位专注于学术论文评估的专家。
            你的主要职责是：
            1. 使用多维度指标体系评估论文质量
            2. 确保论文的可靠性和创新性
            3. 提供具体的改进建议
            4. 评估论文的学术价值
            
            当前评估标准：
            {self.evaluation_criteria}
            
            请基于以下上下文提供专业的评估意见：
            {context}
            """
            
            response = await self.generate_response(message, system_prompt)
            
            evaluation = {
                "type": "paper_evaluation",
                "content": response,
                "timestamp": "current_time"
            }
            self.evaluation_history.append(evaluation)
            
            return response
        except Exception as e:
            print(f"Error in Evaluator agent: {e}")
            return f"Error generating response: {str(e)}"

    def evaluate_paper(self, paper_content: Dict[str, str]) -> Dict[str, Any]:
        """评估论文质量"""
        evaluation = {
            "overall_score": 0.0,
            "detailed_scores": self.evaluation_criteria.copy(),
            "strengths": [],
            "weaknesses": [],
            "improvement_suggestions": []
        }
        
        self.evaluation_history.append({
            "type": "full_evaluation",
            "content": evaluation,
            "timestamp": "current_time"
        })
        
        return evaluation

    def update_criteria(self, category: str, criteria: Dict[str, float]):
        """更新评估标准"""
        if category in self.evaluation_criteria:
            self.evaluation_criteria[category].update(criteria)

    def get_evaluation_history(self) -> List[Dict[str, Any]]:
        """获取所有评估历史"""
        return self.evaluation_history 