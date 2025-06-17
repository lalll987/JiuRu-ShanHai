from typing import Dict, List, Any
from dashscope import Generation

class ContentWriter:
    def __init__(self):
        self.writing_history: List[Dict[str, Any]] = []

    async def write_content(self, topic: str, outline: Dict[str, Any], section: str) -> Dict[str, Any]:
        """撰写论文内容"""
        try:
            system_prompt = """你是一位学术写作专家。
            请根据研究主题和大纲，撰写论文的指定部分，要求：
            1. 学术性强
            2. 逻辑清晰
            3. 论证充分
            4. 语言准确
            5. 格式规范
            """
            
            response = await Generation.call(
                model='qwen-max',
                prompt=f"{system_prompt}\n\n研究主题：{topic}\n\n大纲：{outline['outline']}\n\n需要撰写的部分：{section}",
                temperature=0.7,
                max_tokens=2000
            )
            
            content = {
                "topic": topic,
                "outline": outline,
                "section": section,
                "content": response.output.text,
                "timestamp": "current_time"
            }
            self.writing_history.append(content)
            
            return content
        except Exception as e:
            print(f"Error in content writing: {e}")
            return {"error": str(e)}

    def get_writing_history(self) -> List[Dict[str, Any]]:
        """获取写作历史"""
        return self.writing_history 