# The Musical Bible (TMB) - n8n Dockerfile
# Railway 배포용

FROM n8n/n8n:latest

# 시스템 패키지 업데이트 및 필수 도구 설치
USER root

RUN apt-get update && apt-get install -y \
    ffmpeg \
    python3 \
    python3-pip \
    sqlite3 \
    curl \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Python 패키지 설치
RUN pip3 install --no-cache-dir \
    Pillow \
    requests

# 작업 디렉토리 설정
WORKDIR /data

# 스크립트 복사
COPY scripts/ /data/scripts/
COPY database/ /data/database/

# 스크립트 실행 권한 부여
RUN chmod +x /data/scripts/ffmpeg_compose.sh
RUN chmod +x /data/scripts/generate_thumbnail.py

# n8n 사용자로 전환
USER node

# 환경 변수 설정
ENV N8N_BASIC_AUTH_ACTIVE=true
ENV N8N_HOST=0.0.0.0
ENV N8N_PORT=5678
ENV N8N_PROTOCOL=https
ENV N8N_NODES_INCLUDE=n8n-nodes-base.executeCommand

# 포트 노출
EXPOSE 5678

# n8n 시작
CMD ["n8n", "start"]
