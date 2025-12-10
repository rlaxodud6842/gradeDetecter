# Python 3.12 기반의 슬림 이미지 사용
FROM python:3.12-slim

ENV DEBIAN_FRONTEND=noninteractive

# 크롬 및 chromedriver 설치
RUN apt-get update && apt-get install -y \
    chromium \
    chromium-driver \
    libglib2.0-0 \
    libnss3 \
    libx11-xcb1 \
    libxcomposite1 \
    libxdamage1 \
    libxrandr2 \
    libasound2 \
    libatk-bridge2.0-0 \
    libgtk-3-0 \
    libgbm-dev \
    wget \
    unzip \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# 작업 디렉터리
WORKDIR /app
COPY . .

# 의존성 설치
RUN pip install uv
RUN uv venv .venv
RUN uv pip install -r requirements.txt

CMD ["uv", "run", "python", "main.py"]

