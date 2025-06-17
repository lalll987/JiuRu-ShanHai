import subprocess
import webbrowser
import time
import os
from http.server import HTTPServer, SimpleHTTPRequestHandler
import threading

def start_backend():
    """启动后端Flask服务器"""
    subprocess.Popen(['python', 'app.py'])

def start_frontend_server():
    """启动前端静态文件服务器"""
    os.chdir('frontend')  # 切换到frontend目录
    server = HTTPServer(('localhost', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()

def main():
    # 启动后端服务器
    print("正在启动后端服务器...")
    start_backend()
    
    # 等待后端服务器启动
    time.sleep(2)
    
    # 启动前端服务器
    print("正在启动前端服务器...")
    frontend_thread = threading.Thread(target=start_frontend_server)
    frontend_thread.daemon = True
    frontend_thread.start()
    
    # 等待前端服务器启动
    time.sleep(1)
    
    # 在默认浏览器中打开前端页面
    print("正在打开浏览器...")
    webbrowser.open('http://localhost:8000')
    
    print("\n系统已启动！")
    print("前端地址: http://localhost:8000")
    print("后端地址: http://localhost:5000")
    print("\n按Ctrl+C可以停止服务器")
    
    try:
        # 保持主线程运行
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n正在关闭服务器...")

if __name__ == '__main__':
    main() 