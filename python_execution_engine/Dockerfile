FROM python:3.11-slim

# 设置工作目录
WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    curl \
    sudo \
    && rm -rf /var/lib/apt/lists/*

# 复制requirements文件
COPY requirements.txt .

# 安装Python依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制应用代码
COPY . .

# 创建workspace目录和必要的临时目录
RUN mkdir -p /app/workspace /tmp/mpl_config /tmp/pip_cache

# 设置目录权限
RUN chmod +x run.py && \
    chmod 777 /tmp/mpl_config && \
    chmod 777 /tmp/pip_cache && \
    chmod 777 /app/workspace

# 设置环境变量
ENV MPLCONFIGDIR=/tmp/mpl_config
ENV PIP_CACHE_DIR=/tmp/pip_cache

# 暴露端口
EXPOSE 5000

# 健康检查
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5000/health || exit 1

# 启动命令（以root权限运行）
CMD ["python", "run.py"]