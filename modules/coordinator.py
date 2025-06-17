from typing import Dict, Any, List
from dashscope import Generation
from .research_analyzer import ResearchAnalyzer
from .file_processor import FileProcessor

# 设置API密钥
Generation.set_api_key('sk-tatviaawpkyenqcmgdpjbmmsmaivxxdgnnjxtdwbnycjnunu')

class Coordinator:
    def __init__(self):
        self.research_analyzer = ResearchAnalyzer()
        self.file_processor = FileProcessor()
        self.model = 'qwen-max'
        self.temperature = 0.7
        self.max_tokens = 2000

    async def process_request(self, message: str, files: List[Dict[str, str]] = None) -> Dict[str, Any]:
        """处理用户请求并协调各个模块"""
        try:
            # 处理文件
            file_results = None
            if files:
                file_results = await self.file_processor.process_files(files)

            # 分析研究想法
            research_analysis = await self.research_analyzer.analyze_research(
                message,
                context=file_results
            )

            # 生成综合建议
            final_response = await self._generate_final_response(
                message,
                research_analysis,
                file_results
            )

            return {
                'response': final_response,
                'status': 'success',
                'file_analysis': file_results,
                'research_analysis': research_analysis
            }

        except Exception as e:
            return {
                'error': str(e),
                'status': 'error'
            }

    async def _generate_final_response(self, message: str, research_analysis: Dict[str, Any], file_results: Dict[str, Any] = None) -> str:
        """生成最终的综合建议"""
        try:
            prompt = self._build_final_prompt(message, research_analysis, file_results)
            
            response = Generation.call(
                model=self.model,
                prompt=prompt,
                temperature=self.temperature,
                max_tokens=self.max_tokens
            )

            if response.status_code == 200:
                return response.output.text
            else:
                return f"生成建议时出错: {response.status_code}"

        except Exception as e:
            return f"生成建议时出错: {str(e)}"

    def _build_final_prompt(self, message: str, research_analysis: Dict[str, Any], file_results: Dict[str, Any] = None) -> str:
        """构建最终建议的提示词"""
        prompt = f"""基于以下信息，请提供综合性的研究建议：

研究想法：
{message}

研究分析：
{research_analysis.get('analysis', '无分析结果')}"""

        if file_results and file_results.get('files'):
            prompt += "\n\n文件分析："
            for file in file_results['files']:
                if file.get('analysis'):
                    prompt += f"\n{file['filename']}: {file['analysis']}"

        prompt += "\n\n请提供：\n1. 研究建议总结\n2. 下一步行动建议\n3. 潜在风险提示"

        return prompt 