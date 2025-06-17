import asyncio
from typing import Dict, List, Any
from agents.phd_agent import PhDAgent
from agents.dr_agent import DrAgent
from agents.writer_agent import WriterAgent
from agents.evaluator_agent import EvaluatorAgent
from modules.thesis_evaluation import ThesisEvaluationModule
from modules.research_analyzer import ResearchAnalyzer
from modules.literature_review import LiteratureReviewModule
from modules.research_executor import ResearchExecutor
from core.coordinator import Coordinator
from modules.file_processor import FileProcessor
import os
import logging

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ThesisWritingSystem:
    def __init__(self):
        # 初始化协调器
        self.coordinator = Coordinator()
        
        # 初始化智能体
        self.phd_agent = PhDAgent(coordinator=self.coordinator)
        self.dr_agent1 = DrAgent(name="Dr Agent 1", coordinator=self.coordinator)
        self.dr_agent2 = DrAgent(name="Dr Agent 2", coordinator=self.coordinator)
        self.writer_agent = WriterAgent(coordinator=self.coordinator)
        self.evaluator_agent = EvaluatorAgent(coordinator=self.coordinator)
        
        # 初始化模块
        self.evaluation_module = ThesisEvaluationModule()
        self.research_analyzer = ResearchAnalyzer()
        self.literature_review = LiteratureReviewModule()
        self.research_executor = ResearchExecutor()
        
        # 系统状态
        self.current_stage = "initialization"
        self.research_topic = None
        self.conversation_id = None

    async def process_research_topic(self, topic: str):
        """处理研究主题"""
        try:
            # 创建新的对话
            self.conversation_id = self.coordinator.create_conversation(topic)
            self.research_topic = topic
            
            # 设置所有智能体的对话ID
            self.phd_agent.set_conversation(self.conversation_id)
            self.dr_agent1.set_conversation(self.conversation_id)
            self.dr_agent2.set_conversation(self.conversation_id)
            self.writer_agent.set_conversation(self.conversation_id)
            self.evaluator_agent.set_conversation(self.conversation_id)
            
            # 并行获取Dr Agents的分析
            dr1_analysis = await self.dr_agent1.analyze_research_status(topic)
            dr2_analysis = await self.dr_agent2.analyze_research_status(topic)
            
            # PhD Agent基于分析更新研究框架
            framework_update = {
                "research_question": f"基于{dr1_analysis['research_gaps']}和{dr2_analysis['research_gaps']}的研究空白",
                "theoretical_framework": "待完善",
                "methodology": "待确定",
                "expected_contributions": "待明确"
            }
            
            for section, content in framework_update.items():
                self.phd_agent.update_framework(section, content)
            
            return {
                "status": "success",
                "framework": self.phd_agent.get_framework_status(),
                "dr1_analysis": dr1_analysis,
                "dr2_analysis": dr2_analysis
            }
            
        except Exception as e:
            logger.error(f"Error processing research topic: {e}")
            return {
                "status": "error",
                "message": str(e)
            }

    async def process_message(self, message: str) -> Dict[str, Any]:
        """处理用户消息"""
        try:
            # 获取所有智能体的响应
            responses = await asyncio.gather(
                self.phd_agent.process_message(message),
                self.dr_agent1.process_message(message),
                self.dr_agent2.process_message(message),
                self.writer_agent.process_message(message),
                self.evaluator_agent.process_message(message)
            )
            
            return {
                "status": "success",
                "responses": {
                    "phd_agent": responses[0],
                    "dr_agent1": responses[1],
                    "dr_agent2": responses[2],
                    "writer_agent": responses[3],
                    "evaluator_agent": responses[4]
                }
            }
            
        except Exception as e:
            logger.error(f"Error processing message: {e}")
            return {
                "status": "error",
                "message": str(e)
            }

    def get_system_status(self) -> Dict[str, Any]:
        """获取系统状态"""
        return {
            "current_stage": self.current_stage,
            "research_topic": self.research_topic,
            "conversation_id": self.conversation_id,
            "phd_agent": self.phd_agent.get_framework_status(),
            "writer_agent": self.writer_agent.get_paper_status(),
            "evaluator_agent": self.evaluator_agent.evaluation_criteria
        }

async def main():
    # 创建系统实例
    system = ThesisWritingSystem()
    
    # 选择输入模式
    print("请选择研究主题输入模式：")
    print("1. 输入具体研究想法")
    print("2. 输入参考文献")
    choice = input("请输入选项（1或2）：")
    
    if choice == "1":
        research_idea = input("\n请输入您的研究想法：")
        result = await system.process_research_topic(research_idea)
    else:
        print("\n请输入参考文献（每行一篇，输入空行结束）：")
        references = []
        while True:
            ref = input()
            if not ref:
                break
            references.append(ref)
        result = await system.process_research_topic(references[0])
    
    if result["status"] == "success":
        print("\n=== 研究框架开发完成 ===")
        print("\n研究框架：")
        print(result["framework"])
        
        print("\nDr Agent 1 分析：")
        print(result["dr1_analysis"])
        
        print("\nDr Agent 2 分析：")
        print(result["dr2_analysis"])
        
        # 进入交互式对话模式
        print("\n=== 进入交互式对话模式 ===")
        print("您可以与系统进行对话，输入'quit'退出")
        
        while True:
            message = input("\n请输入您的问题或指令：")
            if message.lower() == 'quit':
                break
                
            response = await system.process_message(message)
            if response["status"] == "success":
                print("\nPhD Agent 响应：")
                print(response["responses"]["phd_agent"])
                
                print("\nDr Agent 1 响应：")
                print(response["responses"]["dr_agent1"])
                
                print("\nDr Agent 2 响应：")
                print(response["responses"]["dr_agent2"])
                
                print("\nWriter Agent 响应：")
                print(response["responses"]["writer_agent"])
                
                print("\nEvaluator Agent 响应：")
                print(response["responses"]["evaluator_agent"])
            else:
                print(f"错误：{response['message']}")
    
    else:
        print(f"错误：{result['message']}")

if __name__ == "__main__":
    asyncio.run(main()) 