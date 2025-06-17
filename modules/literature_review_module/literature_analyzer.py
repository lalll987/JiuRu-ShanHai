from typing import Dict, List, Any
from dashscope import Generation

class LiteratureAnalyzer:
    def __init__(self):
        self.analysis_history: List[Dict[str, Any]] = []

    async def analyze_literature(self, topic: str, papers: List[Dict[str, Any]]) -> Dict[str, Any]:
        """分析文献内容"""
        try:
            system_prompt = """你是一位文献分析专家。
            请根据研究主题和文献内容，进行深入分析，包括：
            1. 文献综述
            2. 主要观点
            3. 研究方法
            4. 研究结论
            5. 研究贡献
            """
            
            papers_text = "\n\n".join([f"论文{i+1}：{paper['content']}" for i, paper in enumerate(papers)])
            
            response = await Generation.call(
                model='qwen-max',
                prompt=f"{system_prompt}\n\n研究主题：{topic}\n\n文献内容：\n{papers_text}",
                temperature=0.7,
                max_tokens=2000
            )
            
            analysis_result = {
                "topic": topic,
                "papers": papers,
                "analysis": response.output.text,
                "timestamp": "current_time"
            }
            self.analysis_history.append(analysis_result)
            
            return analysis_result
        except Exception as e:
            print(f"Error in literature analysis: {e}")
            return {"error": str(e)}

    def get_analysis_history(self) -> List[Dict[str, Any]]:
        """获取文献分析历史"""
        return self.analysis_history 