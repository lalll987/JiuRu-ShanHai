from typing import Dict, List, Any
from dashscope import Generation
import json
import asyncio
from datetime import datetime

class LiteratureReviewModule:
    def __init__(self):
        self.review_history: List[Dict[str, Any]] = []
        self.collected_papers: List[Dict[str, Any]] = []
        self.filtered_papers: List[Dict[str, Any]] = []
        self.idea_generation_results: List[Dict[str, Any]] = []

    async def collect_resources(self, topic: str) -> List[Dict[str, Any]]:
        """通过MCP收集研究资源"""
        system_prompt = """你是一个专业的学术资源收集助手。
        请基于给定的研究主题，从以下方面收集相关资源：
        1. 核心学术论文
        2. 相关研究综述
        3. 重要理论文献
        4. 研究方法文献
        5. 最新研究进展
        
        对于每篇文献，请提供：
        - 标题
        - 作者
        - 发表年份
        - 期刊/会议名称
        - 引用次数
        - 摘要
        - 关键词
        - 研究方法
        - 主要发现
        - 研究局限
        - 未来研究方向"""

        try:
            response = Generation.call(
                model='qwen-vl-plus',
                prompt=f"{system_prompt}\n\n研究主题：{topic}",
                temperature=0.7,
                max_tokens=2000
            )
            
            # 解析响应并构建论文列表
            papers = self._parse_papers_from_response(response.output.text)
            self.collected_papers.extend(papers)
            
            collection_record = {
                "type": "resource_collection",
                "topic": topic,
                "papers": papers,
                "timestamp": datetime.now().isoformat()
            }
            self.review_history.append(collection_record)
            
            return papers
            
        except Exception as e:
            print(f"Error collecting resources: {e}")
            return []

    def filter_resources(self, papers: List[Dict[str, Any]], 
                        min_citations: int = 10,
                        min_year: int = 2018) -> List[Dict[str, Any]]:
        """基于质量指标筛选资源"""
        filtered_papers = []
        for paper in papers:
            # 计算质量分数
            quality_score = self._calculate_quality_score(paper, min_citations, min_year)
            paper['quality_score'] = quality_score
            
            # 应用筛选标准
            if (paper.get('citations', 0) >= min_citations and
                paper.get('year', 0) >= min_year and
                quality_score >= 0.6):  # 质量分数阈值
                filtered_papers.append(paper)
        
        self.filtered_papers = filtered_papers
        
        filter_record = {
            "type": "resource_filtering",
            "original_count": len(papers),
            "filtered_count": len(filtered_papers),
            "filtered_papers": filtered_papers,
            "timestamp": datetime.now().isoformat()
        }
        self.review_history.append(filter_record)
        
        return filtered_papers

    async def generate_ideas(self, papers: List[Dict[str, Any]]) -> Dict[str, Any]:
        """基于筛选后的资源生成研究创意"""
        # 构建论文分析文本
        papers_text = "\n\n".join([
            f"论文：{paper.get('title', '')}\n"
            f"作者：{', '.join(paper.get('authors', []))}\n"
            f"年份：{paper.get('year', '')}\n"
            f"摘要：{paper.get('abstract', '')}\n"
            f"研究方法：{paper.get('methodology', '')}\n"
            f"主要发现：{paper.get('findings', '')}\n"
            f"研究局限：{paper.get('limitations', '')}\n"
            f"未来方向：{paper.get('future_directions', '')}"
            for paper in papers
        ])

        system_prompt = """你是一个专业的研究创意生成专家。
        请基于提供的论文分析，生成新的研究创意。分析应包括：
        1. 现有研究的局限性分析
        2. 研究方法创新建议
        3. 研究内容扩展建议
        4. 潜在的研究问题
        5. 理论框架创新建议
        6. 具体研究建议
        
        请以结构化的方式输出分析结果。"""

        try:
            response = Generation.call(
                model='qwen-vl-plus',
                prompt=f"{system_prompt}\n\n论文分析：\n{papers_text}",
                temperature=0.7,
                max_tokens=2000
            )
            
            idea_generation = {
                "type": "idea_generation",
                "papers_analyzed": len(papers),
                "analysis": response.output.text,
                "timestamp": datetime.now().isoformat()
            }
            
            self.idea_generation_results.append(idea_generation)
            return idea_generation
            
        except Exception as e:
            print(f"Error generating ideas: {e}")
            return {
                "type": "idea_generation",
                "error": str(e)
            }

    def _calculate_quality_score(self, paper: Dict[str, Any], 
                               min_citations: int, 
                               min_year: int) -> float:
        """计算论文质量分数"""
        # 引用分数 (0-0.4)
        citation_score = min(paper.get('citations', 0) / min_citations, 1.0) * 0.4
        
        # 年份分数 (0-0.3)
        current_year = datetime.now().year
        year_score = min((paper.get('year', 0) - min_year) / (current_year - min_year), 1.0) * 0.3
        
        # 内容完整性分数 (0-0.3)
        content_score = 0.0
        if paper.get('abstract'):
            content_score += 0.1
        if paper.get('methodology'):
            content_score += 0.1
        if paper.get('findings'):
            content_score += 0.1
            
        return citation_score + year_score + content_score

    def _parse_papers_from_response(self, response_text: str) -> List[Dict[str, Any]]:
        """解析模型响应中的论文信息"""
        # 这里需要根据实际响应格式进行解析
        # 示例实现
        papers = []
        try:
            # 假设响应是JSON格式
            papers = json.loads(response_text)
        except:
            # 如果不是JSON格式，尝试其他解析方法
            # 这里需要根据实际响应格式实现具体的解析逻辑
            pass
        return papers

    def get_review_history(self) -> List[Dict[str, Any]]:
        """获取文献综述历史"""
        return self.review_history

    def get_collected_papers(self) -> List[Dict[str, Any]]:
        """获取收集的论文"""
        return self.collected_papers

    def get_filtered_papers(self) -> List[Dict[str, Any]]:
        """获取筛选后的论文"""
        return self.filtered_papers

    def get_idea_generation_results(self) -> List[Dict[str, Any]]:
        """获取创意生成结果"""
        return self.idea_generation_results 