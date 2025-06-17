from typing import Dict, List, Any
from dashscope import Generation

class IdeaGenerator:
    def __init__(self):
        self.idea_history: List[Dict[str, Any]] = []

    async def generate_research_ideas(self, topic: str, gap_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """生成研究想法"""
        try:
            system_prompt = """你是一位研究想法生成专家。
            请根据研究主题和研究空白分析，生成具体的研究想法，包括：
            1. 研究问题
            2. 研究假设
            3. 研究方法
            4. 预期成果
            5. 创新点
            """
            
            response = await Generation.call(
                model='qwen-max',
                prompt=f"{system_prompt}\n\n研究主题：{topic}\n\n研究空白：{gap_analysis['gaps']}",
                temperature=0.7,
                max_tokens=2000
            )
            
            research_ideas = {
                "topic": topic,
                "gap_analysis": gap_analysis,
                "ideas": response.output.text,
                "timestamp": "current_time"
            }
            self.idea_history.append(research_ideas)
            
            return research_ideas
        except Exception as e:
            print(f"Error in idea generation: {e}")
            return {"error": str(e)}

    def get_idea_history(self) -> List[Dict[str, Any]]:
        """获取研究想法历史"""
        return self.idea_history 