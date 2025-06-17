from typing import Dict, List, Any
from dashscope import Generation

class ResearchPlanner:
    def __init__(self):
        self.plan_history: List[Dict[str, Any]] = []

    async def create_research_plan(self, topic: str, requirements: Dict[str, Any]) -> Dict[str, Any]:
        """创建研究计划"""
        try:
            system_prompt = """你是一位研究规划专家。
            请根据研究主题和需求，制定详细的研究计划，包括：
            1. 研究目标
            2. 研究方法
            3. 数据需求
            4. 时间安排
            5. 预期成果
            """
            
            response = await Generation.call(
                model='qwen-max',
                prompt=f"{system_prompt}\n\n研究主题：{topic}\n\n研究需求：{requirements}",
                temperature=0.7,
                max_tokens=2000
            )
            
            research_plan = {
                "topic": topic,
                "requirements": requirements,
                "plan": response.output.text,
                "timestamp": "current_time"
            }
            self.plan_history.append(research_plan)
            
            return research_plan
        except Exception as e:
            print(f"Error in research planning: {e}")
            return {"error": str(e)}

    def get_plan_history(self) -> List[Dict[str, Any]]:
        """获取研究计划历史"""
        return self.plan_history 