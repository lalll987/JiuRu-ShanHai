from typing import Dict, List, Any
from dashscope import Generation

class ResearchExecutor:
    def __init__(self):
        self.execution_history: List[Dict[str, Any]] = []

    async def execute_research(self, topic: str, data: Dict[str, Any], methodology: str) -> Dict[str, Any]:
        """执行研究分析"""
        try:
            system_prompt = """你是一位研究执行专家。
            请根据研究主题、数据和方法论，执行研究分析，包括：
            1. 数据分析
            2. 结果解释
            3. 假设验证
            4. 研究结论
            """
            
            response = await Generation.call(
                model='qwen-max',
                prompt=f"{system_prompt}\n\n研究主题：{topic}\n\n数据：{data}\n\n研究方法：{methodology}",
                temperature=0.7,
                max_tokens=2000
            )
            
            execution_result = {
                "topic": topic,
                "methodology": methodology,
                "results": response.output.text,
                "timestamp": "current_time"
            }
            self.execution_history.append(execution_result)
            
            return execution_result
        except Exception as e:
            print(f"Error in research execution: {e}")
            return {"error": str(e)}

    def get_execution_history(self) -> List[Dict[str, Any]]:
        """获取研究执行历史"""
        return self.execution_history 