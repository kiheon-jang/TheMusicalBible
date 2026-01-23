#!/bin/bash
# The Musical Bible (TMB) - Railway 배포 스크립트

echo "=== The Musical Bible (TMB) Railway 배포 시작 ==="

# Railway CLI 확인
if ! command -v railway &> /dev/null; then
    echo "Railway CLI가 설치되어 있지 않습니다."
    echo "설치 중..."
    npm install -g @railway/cli
fi

# Railway 로그인 확인
if ! railway whoami &> /dev/null; then
    echo "Railway에 로그인하세요:"
    railway login
fi

# 프로젝트 생성 또는 선택
echo "프로젝트 생성 중..."
PROJECT_NAME="The Musical Bible - TMB"
railway init "$PROJECT_NAME" || railway link

# 서비스 배포
echo "서비스 배포 중..."
railway up

# 환경 변수 설정
echo "환경 변수 설정 중..."
railway variables set N8N_BASIC_AUTH_ACTIVE=true
railway variables set N8N_HOST=0.0.0.0
railway variables set N8N_PORT=5678
railway variables set N8N_PROTOCOL=https
railway variables set DB_SQLITE_PATH=/data/database/scripture.db

# n8n 비밀번호 설정 (사용자 입력 필요)
read -sp "n8n 관리자 비밀번호를 입력하세요: " N8N_PASSWORD
echo
railway variables set N8N_BASIC_AUTH_USER=admin
railway variables set N8N_BASIC_AUTH_PASSWORD="$N8N_PASSWORD"

# 볼륨 생성 (데이터 영구 저장)
echo "볼륨 생성 중..."
railway volumes create --name data --mount-path /data

echo "=== 배포 완료 ==="
echo "Railway 대시보드에서 서비스 상태를 확인하세요."
echo "배포된 URL: railway status"
