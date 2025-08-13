# ====== builder ======
FROM docker.m.daocloud.io/library/python:3.10-slim AS builder
ENV DEBIAN_FRONTEND=noninteractive

# 用阿里云镜像（也可换清华，见下）
RUN rm -f /etc/apt/sources.list.d/debian.sources && \
    printf "deb http://mirrors.aliyun.com/debian/ bookworm main contrib non-free non-free-firmware\n\
deb http://mirrors.aliyun.com/debian/ bookworm-updates main contrib non-free non-free-firmware\n\
deb http://mirrors.aliyun.com/debian-security bookworm-security main contrib non-free non-free-firmware\n" \
    > /etc/apt/sources.list

# 国内 pip 源
RUN pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple && \
    pip config set global.trusted-host pypi.tuna.tsinghua.edu.cn

# 构建依赖
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc build-essential default-libmysqlclient-dev \
 && rm -rf /var/lib/apt/lists/*

# venv + 依赖
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
COPY requirements.txt .
COPY migrations migrations
RUN pip install --no-cache-dir --compile -r requirements.txt alembic

# ====== runtime ======
FROM docker.m.daocloud.io/library/python:3.10-slim
ENV DEBIAN_FRONTEND=noninteractive

# 同样切换 APT 源
RUN rm -f /etc/apt/sources.list.d/debian.sources && \
    printf "deb http://mirrors.aliyun.com/debian/ bookworm main contrib non-free non-free-firmware\n\
deb http://mirrors.aliyun.com/debian/ bookworm-updates main contrib non-free non-free-firmware\n\
deb http://mirrors.aliyun.com/debian-security bookworm-security main contrib non-free non-free-firmware\n" \
    > /etc/apt/sources.list

# 运行库 + 健康检查工具
RUN apt-get update && apt-get install -y --no-install-recommends \
    default-libmysqlclient-dev curl \
 && rm -rf /var/lib/apt/lists/*

# 拷贝 venv 与应用
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
WORKDIR /app
COPY . .
ENV PYTHONPATH=/app PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1

EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
