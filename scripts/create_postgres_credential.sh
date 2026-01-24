#!/bin/bash
# n8n PostgreSQL Credential 자동 생성 스크립트

N8N_URL="https://n8n-production-1d6b.up.railway.app"
N8N_API_KEY="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI3NzJmYzIwYy0zY2ZiLTQ2YjUtYTZhZi1hZDEwY2IyNDdlZWQiLCJpc3MiOiJuOG4iLCJhdWQiOiJwdWJsaWMtYXBpIiwiaWF0IjoxNzY5MTQ3OTk1fQ.TNPI1IBGNAz6dKkxaMSPi0Cnf-37Sh7mhqSB-AugO-g"

echo "=== n8n PostgreSQL Credential 생성 시도 ==="

# 방법 1: 내부 네트워크 사용
echo "방법 1: 내부 네트워크로 시도..."
CREDENTIAL_JSON1=$(cat <<EOF
{
  "name": "PostgreSQL DB (Internal)",
  "type": "postgres",
  "data": {
    "host": "postgres.railway.internal",
    "port": 5432,
    "database": "railway",
    "user": "postgres",
    "password": "cSdtWArmQfsLDSnpuKLoIgxHaRyGREXq",
    "allowUnauthorizedCerts": false,
    "ssl": false
  }
}
EOF
)

RESPONSE1=$(curl -X POST "${N8N_URL}/api/v1/credentials" \
  -H "X-N8N-API-KEY: ${N8N_API_KEY}" \
  -H "Content-Type: application/json" \
  -d "${CREDENTIAL_JSON1}" \
  -w "\nHTTP_STATUS:%{http_code}" \
  -s)

HTTP_STATUS1=$(echo "$RESPONSE1" | grep -o "HTTP_STATUS:[0-9]*" | cut -d: -f2)
if [ "$HTTP_STATUS1" = "200" ] || [ "$HTTP_STATUS1" = "201" ]; then
  echo "✅ 내부 네트워크 Credential 생성 성공"
  echo "$RESPONSE1" | grep -v "HTTP_STATUS"
  exit 0
else
  echo "❌ 내부 네트워크 실패 (HTTP $HTTP_STATUS1)"
  echo "$RESPONSE1" | head -5
fi

# 방법 2: 외부 네트워크 + SSL Disable
echo ""
echo "방법 2: 외부 네트워크 (SSL Disable)로 시도..."
CREDENTIAL_JSON2=$(cat <<EOF
{
  "name": "PostgreSQL DB",
  "type": "postgres",
  "data": {
    "host": "maglev.proxy.rlwy.net",
    "port": 15087,
    "database": "railway",
    "user": "postgres",
    "password": "cSdtWArmQfsLDSnpuKLoIgxHaRyGREXq",
    "allowUnauthorizedCerts": true,
    "ssl": false
  }
}
EOF
)

RESPONSE2=$(curl -X POST "${N8N_URL}/api/v1/credentials" \
  -H "X-N8N-API-KEY: ${N8N_API_KEY}" \
  -H "Content-Type: application/json" \
  -d "${CREDENTIAL_JSON2}" \
  -w "\nHTTP_STATUS:%{http_code}" \
  -s)

HTTP_STATUS2=$(echo "$RESPONSE2" | grep -o "HTTP_STATUS:[0-9]*" | cut -d: -f2)
if [ "$HTTP_STATUS2" = "200" ] || [ "$HTTP_STATUS2" = "201" ]; then
  echo "✅ 외부 네트워크 Credential 생성 성공"
  echo "$RESPONSE2" | grep -v "HTTP_STATUS"
  exit 0
else
  echo "❌ 외부 네트워크 실패 (HTTP $HTTP_STATUS2)"
  echo "$RESPONSE2" | head -5
fi

# 방법 3: 외부 네트워크 + SSL Require
echo ""
echo "방법 3: 외부 네트워크 (SSL Require)로 시도..."
CREDENTIAL_JSON3=$(cat <<EOF
{
  "name": "PostgreSQL DB (SSL)",
  "type": "postgres",
  "data": {
    "host": "maglev.proxy.rlwy.net",
    "port": 15087,
    "database": "railway",
    "user": "postgres",
    "password": "cSdtWArmQfsLDSnpuKLoIgxHaRyGREXq",
    "allowUnauthorizedCerts": true,
    "ssl": true
  }
}
EOF
)

RESPONSE3=$(curl -X POST "${N8N_URL}/api/v1/credentials" \
  -H "X-N8N-API-KEY: ${N8N_API_KEY}" \
  -H "Content-Type: application/json" \
  -d "${CREDENTIAL_JSON3}" \
  -w "\nHTTP_STATUS:%{http_code}" \
  -s)

HTTP_STATUS3=$(echo "$RESPONSE3" | grep -o "HTTP_STATUS:[0-9]*" | cut -d: -f2)
if [ "$HTTP_STATUS3" = "200" ] || [ "$HTTP_STATUS3" = "201" ]; then
  echo "✅ SSL Require Credential 생성 성공"
  echo "$RESPONSE3" | grep -v "HTTP_STATUS"
  exit 0
else
  echo "❌ SSL Require 실패 (HTTP $HTTP_STATUS3)"
  echo "$RESPONSE3" | head -5
fi

echo ""
echo "❌ 모든 방법 실패. n8n UI에서 수동 설정이 필요할 수 있습니다."
