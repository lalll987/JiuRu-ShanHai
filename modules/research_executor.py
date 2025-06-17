from typing import Dict, List, Any
from dashscope import Generation
import json
from datetime import datetime

class ResearchExecutor:
    def __init__(self):
        self.research_history: List[Dict[str, Any]] = []
        self.current_stage = None
        self.research_type = None
        self.materials = None
        self.theory_framework = None
        self.research_plan = None
        self.analysis_results = None
        self.verification_results = None
        self.optimization_history = []

    async def start_qualitative_research(self, topic: str, materials: str) -> Dict[str, Any]:
        """启动质性研究流程"""
        self.research_type = "qualitative"
        self.materials = materials
        self.current_stage = "design"
        
        # 设计阶段
        design_result = await self._execute_design_stage(topic, materials)
        self.theory_framework = design_result.get("theory_framework")
        self.research_plan = design_result.get("research_plan")
        
        return {
            "stage": "design",
            "result": design_result
        }

    async def _execute_design_stage(self, topic: str, materials: str) -> Dict[str, Any]:
        """执行设计阶段"""
        system_prompt = """你是一个质性研究设计专家。
        请基于提供的研究主题和材料，完成以下任务：
        1. 材料分析
           - 提取关键概念
           - 识别主要主题
           - 发现潜在模式
        
        2. 理论框架构建
           - 确定理论基础
           - 建立概念关系
           - 形成理论框架
        
        3. 研究方案制定
           - 研究方法选择
           - 分析步骤设计
           - 数据收集计划
           - 时间安排
        
        请以结构化的方式输出分析结果。"""

        try:
            response = Generation.call(
                model='qwen-vl-plus',
                prompt=f"{system_prompt}\n\n研究主题：{topic}\n\n研究材料：\n{materials}",
                temperature=0.7,
                max_tokens=2000
            )
            
            design_result = {
                "type": "design_stage",
                "analysis": response.output.text,
                "timestamp": datetime.now().isoformat()
            }
            
            self.research_history.append(design_result)
            return design_result
            
        except Exception as e:
            print(f"Error in design stage: {e}")
            return {
                "type": "design_stage",
                "error": str(e)
            }

    async def execute_implementation_stage(self) -> Dict[str, Any]:
        """执行实现阶段"""
        self.current_stage = "implementation"
        
        system_prompt = """你是一个质性研究分析专家。
        请基于之前的设计方案和研究材料，完成以下任务：
        1. 研究分析
           - 按照学术论文结构进行分析
           - 包括：引言、文献综述、研究方法、数据分析、讨论、结论
        
        2. 论证过程
           - 理论论证
           - 数据支持
           - 逻辑推理
           - 结论推导
        
        请以学术论文的格式输出分析结果。"""

        try:
            response = Generation.call(
                model='qwen-vl-plus',
                prompt=f"{system_prompt}\n\n理论框架：\n{self.theory_framework}\n\n研究方案：\n{self.research_plan}\n\n研究材料：\n{self.materials}",
                temperature=0.7,
                max_tokens=2000
            )
            
            implementation_result = {
                "type": "implementation_stage",
                "analysis": response.output.text,
                "timestamp": datetime.now().isoformat()
            }
            
            self.analysis_results = implementation_result
            self.research_history.append(implementation_result)
            return implementation_result
            
        except Exception as e:
            print(f"Error in implementation stage: {e}")
            return {
                "type": "implementation_stage",
                "error": str(e)
            }

    async def execute_verification_stage(self) -> Dict[str, Any]:
        """执行验证阶段"""
        self.current_stage = "verification"
        
        system_prompt = """你是一个质性研究验证专家。
        请对研究结果进行验证，包括：
        1. 结论与材料比照
           - 检查结论是否得到材料支持
           - 识别潜在矛盾
           - 评估证据充分性
        
        2. 可靠性评估
           - 内部效度评估
           - 外部效度评估
           - 研究局限性分析
        
        请以结构化的方式输出验证结果。"""

        try:
            response = Generation.call(
                model='qwen-vl-plus',
                prompt=f"{system_prompt}\n\n研究材料：\n{self.materials}\n\n分析结果：\n{self.analysis_results['analysis']}",
                temperature=0.7,
                max_tokens=2000
            )
            
            verification_result = {
                "type": "verification_stage",
                "analysis": response.output.text,
                "timestamp": datetime.now().isoformat()
            }
            
            self.verification_results = verification_result
            self.research_history.append(verification_result)
            return verification_result
            
        except Exception as e:
            print(f"Error in verification stage: {e}")
            return {
                "type": "verification_stage",
                "error": str(e)
            }

    async def execute_optimization_stage(self, content: str, professor_feedback: str, research_feedback: str) -> Dict[str, Any]:
        """执行优化阶段"""
        self.current_stage = "optimization"
        
        system_prompt = """你是一个论文优化专家。
        请基于导师反馈对论文进行优化：
        1. 分析反馈意见
        2. 识别需要改进的部分
        3. 提供具体的修改建议
        4. 生成优化后的内容
        
        请以结构化的方式输出优化结果。"""

        try:
            response = Generation.call(
                model='qwen-vl-plus',
                prompt=f"{system_prompt}\n\n当前内容：\n{content}\n\n教授反馈：\n{professor_feedback}\n\n研究顾问反馈：\n{research_feedback}",
                temperature=0.7,
                max_tokens=2000
            )
            
            optimization_result = {
                "type": "optimization_stage",
                "original_content": content,
                "professor_feedback": professor_feedback,
                "research_feedback": research_feedback,
                "optimized_content": response.output.text,
                "timestamp": datetime.now().isoformat()
            }
            
            self.optimization_history.append(optimization_result)
            return optimization_result
            
        except Exception as e:
            print(f"Error in optimization stage: {e}")
            return {
                "type": "optimization_stage",
                "error": str(e)
            }

    def get_research_history(self) -> List[Dict[str, Any]]:
        """获取研究历史"""
        return self.research_history

    def get_optimization_history(self) -> List[Dict[str, Any]]:
        """获取优化历史"""
        return self.optimization_history

    def get_current_stage(self) -> str:
        """获取当前阶段"""
        return self.current_stage 