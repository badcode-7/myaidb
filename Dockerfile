# 阶段1: 依赖安装阶段 (使用完整镜像)
FROM python:3.10-slim AS builder

# 设置国内pip源
RUN pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple && \
    pip config set global.trusted-host pypi.tuna.tsinghua.edu.cn

# 安装系统依赖
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    build-essential \
    default-libmysqlclient-dev \
    && rm -rf /var/lib/apt/lists/*

# 安装Python依赖
COPY requirements.txt .
RUN pip install --no-cache-dir --compile -r requirements.txt

# 阶段2: 最终运行时镜像 (使用更小的基础镜像)
FROM python:3.10-alpine

# 从构建阶段复制虚拟环境
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# 设置工作目录
WORKDIR /app

# 复制应用代码
COPY . .

# 设置环境变量
ENV PYTHONPATH=/app \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# 暴露端口
EXPOSE 8000

# 启动命令
# 
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]