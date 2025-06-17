from typing import Dict, List, Any
from dashscope import Generation
import json

class KnowledgeAcquisitionModule:
    def __init__(self):
        self.paper_database: List[Dict[str, Any]] = []
        self.search_history: List[Dict[str, Any]] = []

    async def search_papers(self, query: str, max_results: int = 5) -> List[Dict[str, Any]]:
        """Search for relevant academic papers"""
        # In a real implementation, this would connect to academic databases
        # For now, we'll simulate paper search results
        system_prompt = """你是一个研究助手，帮助查找相关的学术论文。
        请提供与搜索查询相匹配的论文的结构化信息。"""

        prompt = f"{system_prompt}\n\n请找到{max_results}篇与以下主题相关的学术论文：{query}"

        try:
            response = Generation.call(
                model='qwen-max',
                prompt=prompt,
                temperature=0.3,
                max_tokens=2000
            )
            
            # Parse the response into structured paper data
            # This is a simplified version - in reality, you'd want more robust parsing
            try:
                papers = json.loads(response.output.text)
            except:
                # Fallback if the response isn't valid JSON
                papers = [{"title": "Sample Paper", "authors": ["Author 1"], "abstract": response.output.text}]

            self.search_history.append({
                "query": query,
                "results": papers,
                "timestamp": "current_time"  # You might want to use actual timestamps
            })

            return papers
        except Exception as e:
            print(f"Error in paper search: {e}")
            return []

    async def consult_llm(self, question: str, context: str = "") -> Dict[str, Any]:
        """Consult with LLM about research-related questions"""
        system_prompt = f"""你是一个研究助手，提供专业知识。
        背景：{context}
        请提供详细的、学术级别的研究问题回答。"""

        try:
            response = Generation.call(
                model='qwen-max',
                prompt=f"{system_prompt}\n\n{question}",
                temperature=0.3,
                max_tokens=2000
            )
            
            return {
                "question": question,
                "answer": response.output.text,
                "context": context,
                "timestamp": "current_time"  # You might want to use actual timestamps
            }
        except Exception as e:
            print(f"Error in LLM consultation: {e}")
            return {
                "question": question,
                "answer": f"Error: {str(e)}",
                "context": context,
                "timestamp": "current_time"
            }

    def add_paper_to_database(self, paper: Dict[str, Any]):
        """Add a paper to the local database"""
        self.paper_database.append(paper)

    def get_paper_database(self) -> List[Dict[str, Any]]:
        """Get all papers in the database"""
        return self.paper_database

    def get_search_history(self) -> List[Dict[str, Any]]:
        """Get history of all paper searches"""
        return self.search_history 