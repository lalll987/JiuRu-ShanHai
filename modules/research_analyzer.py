from typing import Dict, List, Any
from dashscope import Generation
import json
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 设置API密钥
os.environ['DASHSCOPE_API_KEY'] = os.getenv('API_KEY')

class ResearchAnalyzer:
    def __init__(self):
        self.analysis_history: List[Dict[str, Any]] = []
        self.model = 'qwen-max'
        self.temperature = 0.7
        self.max_tokens = 2000

    async def analyze_research_idea(self, idea: str) -> Dict[str, Any]:
        """分析用户提供的研究想法"""
        system_prompt = """你是一位专业的研究主题分析专家。
        请分析用户提供的研究想法，并生成详细的研究实施策略。
        分析应包括以下方面：
        1. 研究主题的可行性和创新性
        2. 理论框架建议
        3. 研究方法建议
        4. 预期研究贡献
        5. 潜在的研究挑战
        6. 具体实施步骤
        请以结构化的方式输出分析结果。"""

        try:
            response = Generation.call(
                model='qwen-vl-plus',
                prompt=f"{system_prompt}\n\n研究想法：{idea}",
                temperature=0.7,
                max_tokens=2000
            )
            
            analysis = {
                "type": "idea_analysis",
                "original_idea": idea,
                "analysis": response.output.text,
                "timestamp": "current_time"  # 实际应用中应使用真实时间戳
            }
            
            self.analysis_history.append(analysis)
            return analysis
            
        except Exception as e:
            print(f"Error analyzing research idea: {e}")
            return {
                "type": "idea_analysis",
                "error": str(e),
                "original_idea": idea
            }

    async def analyze_references(self, references: List[Dict[str, Any]]) -> Dict[str, Any]:
        """分析用户提供的参考文献并生成研究概念"""
        # 构建参考文献文本
        refs_text = "\n\n".join([
            f"标题：{ref.get('title', '')}\n"
            f"作者：{', '.join(ref.get('authors', []))}\n"
            f"摘要：{ref.get('abstract', '')}"
            for ref in references
        ])

        system_prompt = """你是一位专业的研究主题分析专家。
        请分析提供的参考文献，并生成新的研究概念。
        分析应包括以下方面：
        1. 现有研究的主题和趋势
        2. 研究空白和机会
        3. 潜在的研究问题
        4. 建议的研究方向
        5. 理论框架建议
        6. 研究方法建议
        请以结构化的方式输出分析结果。"""

        try:
            response = Generation.call(
                model='qwen-vl-plus',
                prompt=f"{system_prompt}\n\n参考文献：\n{refs_text}",
                temperature=0.7,
                max_tokens=2000
            )
            
            analysis = {
                "type": "reference_analysis",
                "references": references,
                "analysis": response.output.text,
                "timestamp": "current_time"  # 实际应用中应使用真实时间戳
            }
            
            self.analysis_history.append(analysis)
            return analysis
            
        except Exception as e:
            print(f"Error analyzing references: {e}")
            return {
                "type": "reference_analysis",
                "error": str(e),
                "references": references
            }

    def get_analysis_history(self) -> List[Dict[str, Any]]:
        """获取分析历史"""
        return self.analysis_history

    def clear_analysis_history(self):
        """清除分析历史"""
        self.analysis_history = []

    async def analyze_research(self, research_idea: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """分析研究想法并返回建议"""
        try:
            # 构建提示词
            prompt = self._build_prompt(research_idea, context)
            
            # 调用Qwen模型
            response = Generation.call(
                model=self.model,
                prompt=prompt,
                temperature=self.temperature,
                max_tokens=self.max_tokens
            )

            if response.status_code == 200:
                return {
                    'analysis': response.output.text,
                    'status': 'success'
                }
            else:
                return {
                    'error': f"Qwen API error: {response.status_code}",
                    'status': 'error'
                }

        except Exception as e:
            return {
                'error': str(e),
                'status': 'error'
            }

    def _build_prompt(self, research_idea: str, context: Dict[str, Any] = None) -> str:
        """构建分析提示词"""
        prompt = f"""请分析以下研究想法，并提供：
1. 研究价值评估
2. 创新点分析
3. 可行性分析
4. 研究方法建议
5. 潜在挑战和解决方案

研究想法：
{research_idea}"""

        if context and context.get('files'):
            prompt += "\n\n相关文件分析："
            for file in context['files']:
                if file.get('analysis'):
                    prompt += f"\n{file['filename']}: {file['analysis']}"

        return prompt 