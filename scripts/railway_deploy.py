#!/usr/bin/env python3
"""
Railway API를 사용한 Video Processor API 배포 스크립트
Railway API 토큰이 필요합니다.
"""

import requests
import json
import sys
import os

RAILWAY_API_URL = "https://api.railway.app/v1"
RAILWAY_TOKEN = os.getenv("RAILWAY_TOKEN") or input("Railway API Token을 입력하세요: ").strip()

if not RAILWAY_TOKEN:
    print("❌ Railway API Token이 필요합니다.")
    print("\n토큰 생성 방법:")
    print("1. https://railway.app 접속")
    print("2. 프로필 → Account Settings → Tokens")
    print("3. New Token 생성")
    sys.exit(1)

headers = {
    "Authorization": f"Bearer {RAILWAY_TOKEN}",
    "Content-Type": "application/json"
}

def get_projects():
    """프로젝트 목록 가져오기"""
    response = requests.get(f"{RAILWAY_API_URL}/projects", headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"❌ 프로젝트 목록 가져오기 실패: {response.status_code}")
        print(response.text)
        return None

def create_service(project_id, repo_url, root_dir="video-processor-api"):
    """서비스 생성"""
    data = {
        "name": "Video Processor API",
        "source": {
            "repo": repo_url,
            "rootDir": root_dir,
            "branch": "main"
        }
    }
    
    response = requests.post(
        f"{RAILWAY_API_URL}/projects/{project_id}/services",
        headers=headers,
        json=data
    )
    
    if response.status_code in [200, 201]:
        return response.json()
    else:
        print(f"❌ 서비스 생성 실패: {response.status_code}")
        print(response.text)
        return None

if __name__ == "__main__":
    print("=" * 70)
    print("Railway API 배포 시작")
    print("=" * 70)
    
    # 프로젝트 목록 가져오기
    print("\n📋 프로젝트 목록 가져오는 중...")
    projects = get_projects()
    
    if not projects:
        sys.exit(1)
    
    # "The Musical Bible" 프로젝트 찾기
    project = None
    for p in projects.get("projects", []):
        if "musical" in p.get("name", "").lower() or "bible" in p.get("name", "").lower():
            project = p
            break
    
    if not project:
        print("\n⚠️  'The Musical Bible' 프로젝트를 찾을 수 없습니다.")
        print("\n사용 가능한 프로젝트:")
        for p in projects.get("projects", []):
            print(f"  - {p.get('name')} (ID: {p.get('id')})")
        project_id = input("\n프로젝트 ID를 입력하세요: ").strip()
    else:
        project_id = project.get("id")
        print(f"\n✅ 프로젝트 찾음: {project.get('name')} (ID: {project_id})")
    
    # 서비스 생성
    print("\n🚀 서비스 생성 중...")
    repo_url = "kiheon-jang/TheMusicalBible"
    service = create_service(project_id, repo_url, "video-processor-api")
    
    if service:
        print("\n✅ 서비스 생성 완료!")
        print(f"   Service ID: {service.get('id')}")
        print(f"   Name: {service.get('name')}")
        print("\n📝 다음 단계:")
        print("   1. Railway 대시보드에서 배포 상태 확인")
        print("   2. 배포 완료 후 URL 확인")
        print("   3. ./scripts/deploy_video_processor.sh 실행")
    else:
        sys.exit(1)
