#!/bin/bash
# Video Processor API 배포 후 n8n 워크플로우 업데이트 스크립트

echo "=================================="
echo "Video Processor API 배포 후 설정"
echo "=================================="
echo ""

# Railway 배포 URL 입력
read -p "Railway에서 제공한 Video Processor API URL을 입력하세요 (예: https://video-processor-xxxx.up.railway.app): " API_URL

if [ -z "$API_URL" ]; then
    echo "❌ URL이 입력되지 않았습니다."
    exit 1
fi

# URL 정규화 (끝에 / 제거)
API_URL=$(echo "$API_URL" | sed 's/\/$//')

echo ""
echo "📝 n8n 워크플로우 업데이트 중..."
echo "   API URL: $API_URL"
echo ""

# Python 스크립트로 워크플로우 업데이트
python3 << EOF
import requests
import json
import sys

N8N_URL = "https://n8n-production-1d6b.up.railway.app"
N8N_API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI3NzJmYzIwYy0zY2ZiLTQ2YjUtYTZhZi1hZDEwY2IyNDdlZWQiLCJpc3MiOiJuOG4iLCJhdWQiOiJwdWJsaWMtYXBpIiwiaWF0IjoxNzY5Mjc3MzAwfQ.o_-qE1uskNW0ZtuqHKBnjCdtmiA5LD0T4McNEcAPU0U"
WORKFLOW_ID = "QoMfESYU0FCalwdb"
API_URL = "$API_URL"

headers = {
    "X-N8N-API-KEY": N8N_API_KEY,
    "Content-Type": "application/json"
}

# 워크플로우 가져오기
response = requests.get(
    f"{N8N_URL}/api/v1/workflows/{WORKFLOW_ID}",
    headers=headers
)

if response.status_code != 200:
    print(f"❌ 워크플로우 가져오기 실패: {response.status_code}")
    sys.exit(1)

workflow = response.json()

# 노드 업데이트
updated = False
for node in workflow.get("nodes", []):
    if node.get("name") == "FFmpeg: 영상 합성 (API)":
        old_url = node.get("parameters", {}).get("url", "")
        node["parameters"]["url"] = f"{API_URL}/api/compose"
        print(f"✅ FFmpeg 노드 URL 업데이트: {old_url} -> {API_URL}/api/compose")
        updated = True
    elif node.get("name") == "Python: 썸네일 생성 (API)":
        old_url = node.get("parameters", {}).get("url", "")
        node["parameters"]["url"] = f"{API_URL}/api/thumbnail"
        print(f"✅ 썸네일 노드 URL 업데이트: {old_url} -> {API_URL}/api/thumbnail")
        updated = True

if not updated:
    print("⚠️  업데이트할 노드를 찾을 수 없습니다.")
    sys.exit(1)

# 워크플로우 업데이트
response = requests.put(
    f"{N8N_URL}/api/v1/workflows/{WORKFLOW_ID}",
    headers=headers,
    json={
        "name": workflow.get("name"),
        "nodes": workflow.get("nodes"),
        "connections": workflow.get("connections", {}),
        "settings": workflow.get("settings", {})
    }
)

if response.status_code == 200:
    print("")
    print("✅ 워크플로우 업데이트 완료!")
    print("")
    print("다음 단계:")
    print("  1. n8n 브라우저에서 워크플로우 새로고침 (Ctrl+R)")
    print("  2. 나머지 Credentials 연결 확인")
    print("  3. Execute Workflow!")
else:
    print(f"❌ 워크플로우 업데이트 실패: {response.status_code}")
    print(response.text[:500])
    sys.exit(1)
EOF

echo ""
echo "=================================="
