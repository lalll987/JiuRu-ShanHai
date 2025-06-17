# 使用官方 Python 运行时作为父镜像
FROM python:3.9-slim

# 设置容器中的工作目录
WORKDIR /app

# 将 requirements 文件复制到容器中
COPY requirements.txt .

# 安装 requirements.txt 中指定的任何需要的包
RUN pip install --no-cache-dir -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# 将应用程序的其余代码复制到容器中
COPY . .

# 使容器外的世界可以访问端口 5000
EXPOSE 5000

# 运行 app.py 当容器启动时
# 我们使用 host='0.0.0.0' 来确保应用可以从容器外部访问
CMD ["python", "app.py"] 