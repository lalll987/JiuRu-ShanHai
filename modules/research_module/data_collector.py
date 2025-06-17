from typing import Dict, List, Any
from dashscope import Generation

class DataCollector:
    def __init__(self):
        self.collection_history: List[Dict[str, Any]] = []

    async def collect_data(self, topic: str, methodology: str) -> Dict[str, Any]:
        """收集研究数据"""
        try:
            system_prompt = """你是一位数据收集专家。
            请根据研究主题和方法论，设计数据收集方案，包括：
            1. 数据来源
            2. 收集方法
            3. 样本选择
            4. 质量控制
            """
            
            response = await Generation.call(
                model='qwen-max',
                prompt=f"{system_prompt}\n\n研究主题：{topic}\n\n研究方法：{methodology}",
                temperature=0.7,
                max_tokens=2000
            )
            
            collection_plan = {
                "topic": topic,
                "methodology": methodology,
                "plan": response.output.text,
                "timestamp": "current_time"
            }
            self.collection_history.append(collection_plan)
            
            return collection_plan
        except Exception as e:
            print(f"Error in data collection: {e}")
            return {"error": str(e)}

    def get_collection_history(self) -> List[Dict[str, Any]]:
        """获取数据收集历史"""
        return self.collection_history 