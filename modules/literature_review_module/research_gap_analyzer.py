from typing import Dict, List, Any
from dashscope import Generation

class ResearchGapAnalyzer:
    def __init__(self):
        self.gap_analysis_history: List[Dict[str, Any]] = []

    async def analyze_research_gaps(self, topic: str, literature_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """分析研究空白"""
        try:
            system_prompt = """你是一位研究空白分析专家。
            请根据研究主题和文献分析结果，识别研究空白，包括：
            1. 未解决的问题
            2. 研究机会
            3. 潜在的研究方向
            4. 创新点建议
            """
            
            response = await Generation.call(
                model='qwen-max',
                prompt=f"{system_prompt}\n\n研究主题：{topic}\n\n文献分析：{literature_analysis['analysis']}",
                temperature=0.7,
                max_tokens=2000
            )
            
            gap_analysis = {
                "topic": topic,
                "literature_analysis": literature_analysis,
                "gaps": response.output.text,
                "timestamp": "current_time"
            }
            self.gap_analysis_history.append(gap_analysis)
            
            return gap_analysis
        except Exception as e:
            print(f"Error in research gap analysis: {e}")
            return {"error": str(e)}

    def get_gap_analysis_history(self) -> List[Dict[str, Any]]:
        """获取研究空白分析历史"""
        return self.gap_analysis_history 