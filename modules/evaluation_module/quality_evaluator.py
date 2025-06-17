from typing import Dict, List, Any
from dashscope import Generation

class QualityEvaluator:
    def __init__(self):
        self.evaluation_history: List[Dict[str, Any]] = []

    async def evaluate_quality(self, topic: str, content: Dict[str, Any]) -> Dict[str, Any]:
        """评估论文质量"""
        try:
            system_prompt = """你是一位论文质量评估专家。
            请根据研究主题和论文内容，评估论文质量，包括：
            1. 学术性
            2. 创新性
            3. 逻辑性
            4. 完整性
            5. 规范性
            6. 改进建议
            """
            
            response = await Generation.call(
                model='qwen-max',
                prompt=f"{system_prompt}\n\n研究主题：{topic}\n\n论文内容：{content['content']}",
                temperature=0.7,
                max_tokens=2000
            )
            
            evaluation = {
                "topic": topic,
                "content": content,
                "evaluation": response.output.text,
                "timestamp": "current_time"
            }
            self.evaluation_history.append(evaluation)
            
            return evaluation
        except Exception as e:
            print(f"Error in quality evaluation: {e}")
            return {"error": str(e)}

    def get_evaluation_history(self) -> List[Dict[str, Any]]:
        """获取评估历史"""
        return self.evaluation_history 