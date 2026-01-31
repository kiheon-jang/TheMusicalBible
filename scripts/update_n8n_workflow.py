#!/usr/bin/env python3
"""
n8n 스토리 파이프라인 워크플로우를 로컬 JSON으로 덮어씁니다.
youtube 노드 제거 버전으로 업데이트하여 "Unrecognized node type: n8n-nodes-base.youtube" 해결.

사용: export N8N_API_KEY=your_key && python3 scripts/update_n8n_workflow.py
"""
import json
import os
import sys

import urllib.request
import urllib.error

N8N_URL = os.environ.get("N8N_URL", "https://n8n-production-1d6b.up.railway.app")
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
WORKFLOW_PATH = os.path.join(PROJECT_ROOT, "workflows", "complete_pipeline_story.json")
API_KEYS_PATH = os.path.join(PROJECT_ROOT, "API_KEYS.txt")


def _load_api_key():
    """환경 변수 또는 API_KEYS.txt에서 N8N API 키 로드."""
    key = os.environ.get("N8N_API_KEY", "").strip()
    if key:
        return key
    if os.path.isfile(API_KEYS_PATH):
        with open(API_KEYS_PATH, "r", encoding="utf-8") as f:
            in_n8n_section = False
            for line in f:
                line = line.strip()
                if "n8n" in line.lower() and ("api" in line.lower() or "##" in line):
                    in_n8n_section = True
                    continue
                if in_n8n_section and line.startswith("##"):
                    break
                if in_n8n_section and line and not line.startswith("#") and line.startswith("eyJ"):
                    return line.strip()
    return ""


def main():
    api_key = _load_api_key()
    if not api_key:
        print("N8N_API_KEY가 없습니다.")
        print("1) n8n 대시보드 > 설정 > API에서 API 키 발급")
        print("2) API_KEYS.txt에 '## n8n API' 섹션 추가 후 그 다음 줄에 키 붙여넣기")
        print("   또는: export N8N_API_KEY=your_key")
        print("3) python3 scripts/update_n8n_workflow.py")
        return 1

    if not os.path.isfile(WORKFLOW_PATH):
        print(f"워크플로우 파일 없음: {WORKFLOW_PATH}")
        return 1

    with open(WORKFLOW_PATH, "r", encoding="utf-8") as f:
        wf = json.load(f)

    node_types = {n.get("type") for n in wf.get("nodes", [])}
    if "n8n-nodes-base.youtube" in node_types:
        print("로컬 JSON에 youtube 노드가 있습니다. workflows/complete_pipeline_story.json 을 수정된 버전으로 교체하세요.")
        return 1

    # 워크플로우 목록
    req = urllib.request.Request(
        f"{N8N_URL}/api/v1/workflows",
        headers={"X-N8N-API-KEY": api_key, "Accept": "application/json"},
        method="GET",
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as res:
            data = json.loads(res.read().decode())
    except urllib.error.HTTPError as e:
        print(f"워크플로우 목록 조회 실패: {e.code} {e.reason}")
        if e.code == 401:
            print("API 키가 잘못되었거나 만료되었습니다.")
        print(e.read().decode()[:400])
        return 1
    except Exception as e:
        print(f"요청 실패: {e}")
        return 1

    workflows = data.get("data", []) if isinstance(data, dict) else data
    if not workflows:
        print("등록된 워크플로우가 없습니다.")
        return 1

    target = None
    for w in workflows:
        name = (w.get("name") or "").lower()
        if "스토리" in (w.get("name") or "") or "story" in name or "complete pipeline" in name:
            target = w
            break
    if not target:
        target = workflows[0]

    wid = target["id"]
    name = target.get("name", wid)
    print(f"업데이트 대상: {name} (ID: {wid})")

    # credential은 로컬 JSON 기준으로만 사용 (다른 인스턴스 encryptionKey 이슈 방지)
    body = json.dumps({
        "name": wf.get("name", name),
        "nodes": wf["nodes"],
        "connections": wf.get("connections", {}),
        "settings": wf.get("settings", {}),
    }).encode("utf-8")

    req2 = urllib.request.Request(
        f"{N8N_URL}/api/v1/workflows/{wid}",
        data=body,
        headers={
            "X-N8N-API-KEY": api_key,
            "Content-Type": "application/json",
            "Accept": "application/json",
        },
        method="PUT",
    )
    try:
        with urllib.request.urlopen(req2, timeout=30) as res:
            json.loads(res.read().decode())
        print("워크플로우 업데이트 완료. n8n에서 해당 워크플로우를 열어 저장 후 실행하세요.")
        return 0
    except urllib.error.HTTPError as e:
        print(f"업데이트 실패: {e.code} {e.reason}")
        print(e.read().decode()[:500])
        return 1
    except Exception as e:
        print(f"오류: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
