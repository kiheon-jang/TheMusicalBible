FROM python:3.11-slim

# 시스템 패키지 설치
RUN apt-get update && apt-get install -y \
    ffmpeg \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Python 패키지 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 애플리케이션 코드
COPY main.py .

# 스크립트 복사
COPY scripts/ /data/scripts/
RUN chmod +x /data/scripts/ffmpeg_compose.sh && \
    chmod +x /data/scripts/generate_thumbnail.py

# 출력 디렉토리
RUN mkdir -p /tmp/tmb_output

EXPOSE 8000

CMD ["python", "main.py"]
