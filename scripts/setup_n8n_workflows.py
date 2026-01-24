#!/usr/bin/env python3
"""
n8n 워크플로우 자동 생성 스크립트
n8n에 로그인하고 워크플로우를 자동으로 생성합니다.
"""

import requests
import json
import os
import sys

N8N_URL = "https://n8n-production-1d6b.up.railway.app"
N8N_USER = "admin"
N8N_PASS = "TMB2026Secure!ChangeMe"

def login_n8n():
    """n8n에 로그인하고 세션 쿠키를 얻습니다."""
    session = requests.Session()
    
    # 로그인 페이지 접속 (CSRF 토큰 얻기)
    login_page = session.get(f"{N8N_URL}/login")
    
    # 로그인 요청
    login_data = {
        "email": N8N_USER,
        "password": N8N_PASS
    }
    
    login_response = session.post(
        f"{N8N_URL}/rest/login",
        json=login_data,
        headers={"Content-Type": "application/json"}
    )
    
    if login_response.status_code == 200:
        print("✅ n8n 로그인 성공")
        return session
    else:
        print(f"❌ 로그인 실패: {login_response.status_code}")
        print(login_response.text)
        return None

def create_workflow(session, workflow_file):
    """워크플로우를 생성합니다."""
    workflow_name = os.path.basename(workflow_file).replace('.json', '')
    
    try:
        with open(workflow_file, 'r', encoding='utf-8') as f:
            workflow_data = json.load(f)
        
        # n8n API 형식에 맞게 변환
        # credentials는 나중에 설정하도록 제거
        for node in workflow_data.get('nodes', []):
            if 'credentials' in node:
                # credentials ID를 제거 (나중에 수동 설정)
                node['credentials'] = {}
        
        response = session.post(
            f"{N8N_URL}/api/v1/workflows",
            json=workflow_data,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code in [200, 201]:
            result = response.json()
            print(f"✅ {workflow_name} 워크플로우 생성 성공 (ID: {result.get('id', 'N/A')})")
            return True
        else:
            print(f"❌ {workflow_name} 워크플로우 생성 실패: {response.status_code}")
            print(response.text)
            return False
            
    except Exception as e:
        print(f"❌ {workflow_name} 워크플로우 생성 중 오류: {e}")
        return False

def main():
    """메인 함수"""
    print("=== n8n 워크플로우 자동 생성 시작 ===\n")
    
    # n8n 로그인
    session = login_n8n()
    if not session:
        print("로그인 실패. 종료합니다.")
        sys.exit(1)
    
    # 워크플로우 파일 목록
    workflow_files = [
        "workflows/init_database.json",
        "workflows/morning_batch.json",
        "workflows/evening_generation.json",
        "workflows/daily_monitoring.json"
    ]
    
    # 각 워크플로우 생성
    success_count = 0
    for workflow_file in workflow_files:
        if os.path.exists(workflow_file):
            if create_workflow(session, workflow_file):
                success_count += 1
        else:
            print(f"⚠️  파일을 찾을 수 없습니다: {workflow_file}")
    
    print(f"\n=== 완료: {success_count}/{len(workflow_files)} 워크플로우 생성 성공 ===")
    print(f"n8n 대시보드에서 확인하세요: {N8N_URL}")

if __name__ == "__main__":
    main()
