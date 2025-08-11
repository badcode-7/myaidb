FROM docker.m.daocloud.io/library/python:3.10-slim AS builder

# 切换到阿里源
RUN sed -i 's@deb.debian.org@mirrors.aliyun.com@g' /etc/apt/sources.list && \
    sed -i 's@security.debian.org@mirrors.aliyun.com@g' /etc/apt/sources.list

RUN pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple \
 && pip config set global.trusted-host pypi.tuna.tsinghua.edu.cn

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc build-essential default-libmysqlclient-dev \
 && rm -rf /var/lib/apt/lists/*

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt .
RUN pip install --no-cache-dir --compile -r requirements.txt

# -------------------
FROM docker.m.daocloud.io/library/python:3.10-slim

# 切换到阿里源
RUN sed -i 's@deb.debian.org@mirrors.aliyun.com@g' /etc/apt/sources.list && \
    sed -i 's@security.debian.org@mirrors.aliyun.com@g' /etc/apt/sources.list

RUN apt-get update && apt-get install -y --no-install-recommends \
    default-libmysqlclient-dev curl \
 && rm -rf /var/lib/apt/lists/*

COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

WORKDIR /app
COPY . .

ENV PYTHONPATH=/app \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
