#!/bin/bash
# YouTube OAuth2 환경 변수 설정 스크립트

echo "=" | head -c 70 && echo ""
echo "📋 YouTube OAuth2 Railway 환경 변수 설정"
echo "=" | head -c 70 && echo ""

CLIENT_ID="1053902423625-6dlr4lgb58e20d0nteaq16ufrnaj7hq0.apps.googleusercontent.com"
CLIENT_SECRET="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"

echo ""
echo "✅ 다음 환경 변수를 Railway n8n 서비스에 추가하세요:"
echo ""
echo "YOUTUBE_CLIENT_ID=$CLIENT_ID"
echo "YOUTUBE_CLIENT_SECRET=$CLIENT_SECRET"
echo "YOUTUBE_ACCESS_TOKEN=<토큰 획득 후 설정>"
echo "YOUTUBE_REFRESH_TOKEN=<토큰 획득 후 설정>"
echo ""
echo "📝 토큰 획득 방법:"
echo "   1. 로컬에서 python3 scripts/get_youtube_token.py 실행"
echo "   2. 브라우저에서 Google 계정 로그인 및 권한 승인"
echo "   3. 출력된 YOUTUBE_ACCESS_TOKEN과 YOUTUBE_REFRESH_TOKEN을 Railway에 설정"
echo ""
echo "=" | head -c 70 && echo ""
