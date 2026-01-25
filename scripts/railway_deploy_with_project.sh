#!/bin/bash
# Railway 프로젝트 ID를 사용한 Video Processor API 배포

PROJECT_ID="b527bba5-9bbe-446a-b192-64194554bad0"

echo "=================================="
echo "Railway Video Processor API 배포"
echo "=================================="
echo ""
echo "프로젝트 ID: $PROJECT_ID"
echo ""

# Railway CLI 확인
if ! command -v railway &> /dev/null; then
    echo "❌ Railway CLI가 설치되어 있지 않습니다."
    echo "설치: npm install -g @railway/cli"
    exit 1
fi

# Railway 로그인 확인
if ! railway whoami &> /dev/null; then
    echo "🔐 Railway 로그인이 필요합니다..."
    railway login
fi

# 프로젝트 연결
echo "📋 프로젝트 연결 중..."
cd video-processor-api
railway link "$PROJECT_ID" 2>&1

# 배포
echo ""
echo "🚀 배포 시작..."
railway up

echo ""
echo "✅ 배포 완료!"
echo ""
echo "📝 다음 단계:"
echo "   1. Railway 대시보드에서 배포 상태 확인"
echo "   2. 배포 완료 후 URL 확인"
echo "   3. ./scripts/deploy_video_processor.sh 실행"
