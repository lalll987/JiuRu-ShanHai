from typing import Dict, List, Any
from dashscope import Generation

class OutlineGenerator:
    def __init__(self):
        self.outline_history: List[Dict[str, Any]] = []

    async def generate_outline(self, topic: str, research_ideas: Dict[str, Any]) -> Dict[str, Any]:
        """生成论文大纲"""
        try:
            system_prompt = """你是一位论文大纲生成专家。
            请根据研究主题和研究想法，生成详细的论文大纲，包括：
            1. 标题
            2. 摘要
            3. 引言
            4. 文献综述
            5. 研究方法
            6. 结果分析
            7. 讨论
            8. 结论
            9. 参考文献
            """
            
            response = await Generation.call(
                model='qwen-max',
                prompt=f"{system_prompt}\n\n研究主题：{topic}\n\n研究想法：{research_ideas['ideas']}",
                temperature=0.7,
                max_tokens=2000
            )
            
            outline = {
                "topic": topic,
                "research_ideas": research_ideas,
                "outline": response.output.text,
                "timestamp": "current_time"
            }
            self.outline_history.append(outline)
            
            return outline
        except Exception as e:
            print(f"Error in outline generation: {e}")
            return {"error": str(e)}

    def get_outline_history(self) -> List[Dict[str, Any]]:
        """获取大纲历史"""
        return self.outline_history 