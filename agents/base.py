import sys
import traceback

class BaseAgent:
    def __init__(self):
        pass

    async def generate_response(self, context: str, prompt: str) -> str:
        try:
            response = await Generation.acall(
                model='qwen-turbo',
                prompt=f"{context}\n\n{prompt}",
                temperature=0.7,
                max_tokens=2000
            )
            # 检查API返回的响应是否成功
            if response.status_code == 200:
                return response.output.text
            else:
                # 如果API返回错误，则将其作为异常信息处理
                error_message = (f"DashScope API Error: Status {response.status_code}, "
                                 f"Code: {response.code}, Message: {response.message}")
                raise Exception(error_message)
        except Exception as e:
            # 捕获所有异常，并将详细信息作为字符串返回
            error_info = f"Caught Exception: {str(e)}\n{traceback.format_exc()}"
            print(error_info, file=sys.stderr) # 再次尝试打印，以防万一
            return error_info

    def set_conversation(self, conversation_id: str):
        """Set the current conversation ID"""
        pass 