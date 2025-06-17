from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import logging
from werkzeug.utils import secure_filename
from dashscope import Generation
from core.coordinator import Coordinator
from agents.professor_advisor import ProfessorAdvisorAgent
from agents.research_advisor import ResearchAdvisorAgent
import asyncio
from functools import wraps

# 配置日志
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# 设置API密钥
api_key = os.environ.get('DASHSCOPE_API_KEY')
if not api_key:
    api_key = 'sk-773c0160d8f04d54a010c7075dcea6c1'
    logger.warning("DASHSCOPE_API_KEY not found in environment variables. Using hardcoded key.")
os.environ['DASHSCOPE_API_KEY'] = api_key

app = Flask(__name__)
# 简化CORS配置
CORS(app)

# 初始化协调器和智能体
try:
    coordinator = Coordinator()
    professor_advisor = ProfessorAdvisorAgent(name="Professor Advisor", coordinator=coordinator)
    research_advisor = ResearchAdvisorAgent(name="Research Advisor", coordinator=coordinator)
except Exception as e:
    logger.error(f"Error initializing coordinator and agents: {e}")
    coordinator = None
    professor_advisor = None
    research_advisor = None

# 配置文件上传
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'doc', 'docx', 'pdf', 'mp4', 'mp3'}

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

async def get_agent_responses(message: str, conversation_id: str):
    """获取所有智能体的响应"""
    try:
        if not coordinator or not professor_advisor or not research_advisor:
            return "系统初始化错误", "系统初始化错误"

        professor_advisor.set_conversation(conversation_id)
        research_advisor.set_conversation(conversation_id)
        
        # 并行获取响应
        professor_response = await professor_advisor.process_message(message)
        research_response = await research_advisor.process_message(message)
        
        return professor_response, research_response
    except Exception as e:
        logger.error(f"Error getting agent responses: {e}")
        return str(e), str(e)

def async_route(f):
    @wraps(f)
    def wrapped(*args, **kwargs):
        return asyncio.run(f(*args, **kwargs))
    return wrapped

@app.route('/api/chat', methods=['POST', 'OPTIONS'])
@async_route
async def chat():
    logger.debug(f"Received request: {request.method}")
    logger.debug(f"Request headers: {request.headers}")
    
    if request.method == 'OPTIONS':
        logger.debug("Handling OPTIONS request")
        return '', 200
        
    try:
        # 获取消息内容
        message = request.form.get('message', '')
        mode = request.form.get('mode')
        conversation_id = request.form.get('conversationId')
        
        if not conversation_id and coordinator:
            conversation_id = coordinator.create_conversation("New Chat")
        elif not conversation_id:
            conversation_id = "temp-" + str(hash(message))
        
        # 将用户消息存入历史记录
        if coordinator:
            user_message = {"role": "user", "content": message}
            coordinator.store_conversation(conversation_id, user_message)
        
        logger.debug(f"Received message: {message}")
        logger.debug(f"Mode: {mode}")
        logger.debug(f"Conversation ID: {conversation_id}")

        # 处理文件上传
        uploaded_files = []
        if 'files' in request.files:
            files = request.files.getlist('files')
            for file in files:
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    file.save(file_path)
                    uploaded_files.append({
                        'name': filename,
                        'path': file_path,
                        'type': filename.rsplit('.', 1)[1].lower()
                    })
                    logger.debug(f"Saved file: {filename}")

        # 获取智能体响应
        professor_feedback, research_feedback = await get_agent_responses(message, conversation_id)

        # 将智能体响应存入历史记录
        if coordinator:
            professor_message = {"role": "assistant", "name": "Professor Advisor", "content": professor_feedback}
            coordinator.store_conversation(conversation_id, professor_message)
            research_message = {"role": "assistant", "name": "Research Advisor", "content": research_feedback}
            coordinator.store_conversation(conversation_id, research_message)

        # 返回响应
        response = {
            'conversationId': conversation_id,
            'analysis': f'收到消息: {message}',
            'professorFeedback': professor_feedback,
            'researchFeedback': research_feedback,
            'fileAnalysis': {
                'files': [{'filename': f['name'], 'analysis': '测试文件分析'} for f in uploaded_files]
            }
        }
        logger.debug(f"Sending response: {response}")
        return jsonify(response)

    except Exception as e:
        logger.error(f"Error in chat endpoint: {str(e)}", exc_info=True)
        return jsonify({
            'error': str(e)
        }), 500

@app.route('/api/test', methods=['GET'])
def test():
    logger.debug("Received test request")
    return jsonify({'status': 'ok', 'message': 'Backend is running'})

if __name__ == '__main__':
    logger.info("Starting server on http://localhost:5000")
    app.run(debug=True, port=5000, host='0.0.0.0') 