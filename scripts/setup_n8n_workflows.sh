#!/bin/bash
# n8n 워크플로우 자동 생성 스크립트

N8N_URL="https://n8n-production-1d6b.up.railway.app"
N8N_API_KEY="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI3NzJmYzIwYy0zY2ZiLTQ2YjUtYTZhZi1hZDEwY2IyNDdlZWQiLCJpc3MiOiJuOG4iLCJhdWQiOiJwdWJsaWMtYXBpIiwiaWF0IjoxNzY5MTQ3OTk1fQ.TNPI1IBGNAz6dKkxaMSPi0Cnf-37Sh7mhqSB-AugO-g"

echo "=== n8n 워크플로우 자동 생성 시작 ==="

# API 형식으로 변환된 파일 사용
python3 scripts/convert_workflow_for_api.py

# 1. 데이터베이스 초기화 워크플로우 생성
echo "1. 데이터베이스 초기화 워크플로우 생성 중..."
RESPONSE1=$(curl -X POST "${N8N_URL}/api/v1/workflows" \
  -H "X-N8N-API-KEY: ${N8N_API_KEY}" \
  -H "Content-Type: application/json" \
  -d @workflows/init_database_api.json \
  -w "\nHTTP_STATUS:%{http_code}" \
  -s)
HTTP_STATUS1=$(echo "$RESPONSE1" | grep -o "HTTP_STATUS:[0-9]*" | cut -d: -f2)
if [ "$HTTP_STATUS1" = "200" ] || [ "$HTTP_STATUS1" = "201" ]; then
  echo "✅ 성공"
else
  echo "❌ 실패 (HTTP $HTTP_STATUS1)"
  echo "$RESPONSE1" | head -5
fi

# 2. Morning Batch 워크플로우 생성
echo "2. Morning Batch 워크플로우 생성 중..."
RESPONSE2=$(curl -X POST "${N8N_URL}/api/v1/workflows" \
  -H "X-N8N-API-KEY: ${N8N_API_KEY}" \
  -H "Content-Type: application/json" \
  -d @workflows/morning_batch_api.json \
  -w "\nHTTP_STATUS:%{http_code}" \
  -s)
HTTP_STATUS2=$(echo "$RESPONSE2" | grep -o "HTTP_STATUS:[0-9]*" | cut -d: -f2)
if [ "$HTTP_STATUS2" = "200" ] || [ "$HTTP_STATUS2" = "201" ]; then
  echo "✅ 성공"
else
  echo "❌ 실패 (HTTP $HTTP_STATUS2)"
  echo "$RESPONSE2" | head -5
fi

# 3. Evening Generation 워크플로우 생성
echo "3. Evening Generation 워크플로우 생성 중..."
RESPONSE3=$(curl -X POST "${N8N_URL}/api/v1/workflows" \
  -H "X-N8N-API-KEY: ${N8N_API_KEY}" \
  -H "Content-Type: application/json" \
  -d @workflows/evening_generation_api.json \
  -w "\nHTTP_STATUS:%{http_code}" \
  -s)
HTTP_STATUS3=$(echo "$RESPONSE3" | grep -o "HTTP_STATUS:[0-9]*" | cut -d: -f2)
if [ "$HTTP_STATUS3" = "200" ] || [ "$HTTP_STATUS3" = "201" ]; then
  echo "✅ 성공"
else
  echo "❌ 실패 (HTTP $HTTP_STATUS3)"
  echo "$RESPONSE3" | head -5
fi

# 4. Daily Monitoring 워크플로우 생성
echo "4. Daily Monitoring 워크플로우 생성 중..."
RESPONSE4=$(curl -X POST "${N8N_URL}/api/v1/workflows" \
  -H "X-N8N-API-KEY: ${N8N_API_KEY}" \
  -H "Content-Type: application/json" \
  -d @workflows/daily_monitoring_api.json \
  -w "\nHTTP_STATUS:%{http_code}" \
  -s)
HTTP_STATUS4=$(echo "$RESPONSE4" | grep -o "HTTP_STATUS:[0-9]*" | cut -d: -f2)
if [ "$HTTP_STATUS4" = "200" ] || [ "$HTTP_STATUS4" = "201" ]; then
  echo "✅ 성공"
else
  echo "❌ 실패 (HTTP $HTTP_STATUS4)"
  echo "$RESPONSE4" | head -5
fi

echo ""
echo "=== 워크플로우 생성 완료 ==="
echo "n8n 대시보드에서 확인하세요: ${N8N_URL}"
