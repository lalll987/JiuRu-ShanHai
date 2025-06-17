import os
from typing import List, Dict, Any
from dashscope import Generation
import PyPDF2
import docx
import json
import aiofiles
import asyncio
import speech_recognition as sr
from pydub import AudioSegment
import logging
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 从环境变量获取API密钥
api_key = os.getenv('API_KEY')
if api_key:
    os.environ['DASHSCOPE_API_KEY'] = api_key
else:
    logger.warning("API_KEY not found in environment variables")

class FileProcessor:
    def __init__(self):
        self.supported_types = {
            'pdf': self._process_pdf,
            'doc': self._process_doc,
            'docx': self._process_doc,
            'mp4': self._process_video,
            'mp3': self._process_audio
        }

    async def process_files(self, files: List[Dict[str, str]]) -> Dict[str, Any]:
        """处理上传的文件并返回分析结果"""
        results = []
        for file in files:
            file_type = file['type'].lower()
            if file_type in self.supported_types:
                try:
                    content = await self.supported_types[file_type](file['path'])
                    analysis = await self._analyze_with_qwen(content, file_type)
                    results.append({
                        'filename': file['name'],
                        'type': file_type,
                        'content': content,
                        'analysis': analysis
                    })
                except Exception as e:
                    logger.error(f"Error processing file {file['name']}: {str(e)}")
                    results.append({
                        'filename': file['name'],
                        'type': file_type,
                        'error': str(e)
                    })
            else:
                logger.warning(f"Unsupported file type: {file_type}")
                results.append({
                    'filename': file['name'],
                    'type': file_type,
                    'error': 'Unsupported file type'
                })
        return {'files': results}

    async def _process_pdf(self, file_path: str) -> str:
        """异步处理PDF文件"""
        async with aiofiles.open(file_path, 'rb') as file:
            content = await file.read()
            pdf_reader = PyPDF2.PdfReader(content)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
            return text

    async def _process_doc(self, file_path: str) -> str:
        """异步处理Word文档"""
        # 由于python-docx不支持异步，使用线程池执行
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self._process_doc_sync, file_path)

    def _process_doc_sync(self, file_path: str) -> str:
        """同步处理Word文档"""
        doc = docx.Document(file_path)
        return "\n".join(paragraph.text for paragraph in doc.paragraphs)

    async def _process_video(self, file_path: str) -> str:
        """异步处理视频文件"""
        try:
            # 使用线程池执行视频处理
            loop = asyncio.get_event_loop()
            return await loop.run_in_executor(None, self._process_video_sync, file_path)
        except Exception as e:
            logger.error(f"Error processing video file: {str(e)}")
            raise

    def _process_video_sync(self, file_path: str) -> str:
        """同步处理视频文件"""
        return "Video processing has been disabled"

    async def _process_audio(self, file_path: str) -> str:
        """异步处理音频文件"""
        try:
            # 使用线程池执行音频处理
            loop = asyncio.get_event_loop()
            return await loop.run_in_executor(None, self._process_audio_sync, file_path)
        except Exception as e:
            logger.error(f"Error processing audio file: {str(e)}")
            raise

    def _process_audio_sync(self, file_path: str) -> str:
        """同步处理音频文件"""
        # 转换音频为WAV格式
        audio = AudioSegment.from_file(file_path)
        audio.export("temp_audio.wav", format="wav")
        
        # 语音转文本
        text = self._speech_to_text("temp_audio.wav")
        
        # 清理临时文件
        os.remove("temp_audio.wav")
        
        duration = len(audio) / 1000.0  # 转换为秒
        return f"""Audio Analysis:
Duration: {duration} seconds
Transcription:
{text}"""

    def _speech_to_text(self, audio_path: str) -> str:
        """将语音转换为文本"""
        recognizer = sr.Recognizer()
        with sr.AudioFile(audio_path) as source:
            audio = recognizer.record(source)
            try:
                return recognizer.recognize_google(audio, language='zh-CN')
            except sr.UnknownValueError:
                return "Speech recognition could not understand the audio"
            except sr.RequestError as e:
                return f"Could not request results from speech recognition service; {str(e)}"

    async def _analyze_with_qwen(self, content: str, file_type: str) -> Dict[str, Any]:
        """使用Qwen模型分析文件内容"""
        try:
            # 构建提示词
            prompt = self._build_prompt(content, file_type)
            
            # 调用Qwen模型
            response = Generation.call(
                model='qwen-max',
                prompt=prompt,
                temperature=0.7,
                max_tokens=2000
            )

            if response.status_code == 200:
                return {
                    'summary': response.output.text,
                    'status': 'success'
                }
            else:
                logger.error(f"Qwen API error: {response.status_code}")
                return {
                    'error': f"Qwen API error: {response.status_code}",
                    'status': 'error'
                }

        except Exception as e:
            logger.error(f"Error analyzing with Qwen: {str(e)}")
            return {
                'error': str(e),
                'status': 'error'
            }

    def _build_prompt(self, content: str, file_type: str) -> str:
        """构建提示词"""
        if file_type in ['pdf', 'doc', 'docx']:
            return f"""请分析以下文档内容，并提供：
1. 主要内容概述
2. 关键观点提取
3. 研究价值评估
4. 相关研究建议

文档内容：
{content}"""
        elif file_type in ['mp4']:
            return f"""请分析以下视频内容，并提供：
1. 视频基本信息分析
2. 语音内容摘要
3. 研究价值评估
4. 使用建议

视频信息：
{content}"""
        else:  # mp3
            return f"""请分析以下音频内容，并提供：
1. 音频基本信息分析
2. 语音内容摘要
3. 研究价值评估
4. 使用建议

音频信息：
{content}""" 