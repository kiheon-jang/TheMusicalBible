#!/usr/bin/env python3
"""
YouTube OAuth2 토큰 획득 스크립트
한 번만 실행하여 Access Token과 Refresh Token을 얻습니다.
"""
import os
import json
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# YouTube API 스코프
SCOPES = ['https://www.googleapis.com/auth/youtube.upload']

def get_youtube_tokens():
    """OAuth2 플로우를 통해 YouTube 토큰 획득"""
    
    # 환경 변수에서 Client ID/Secret 확인
    client_id = os.environ.get('YOUTUBE_CLIENT_ID')
    client_secret = os.environ.get('YOUTUBE_CLIENT_SECRET')
    
    if client_id and client_secret:
        # 환경 변수에서 직접 OAuth2 플로우 시작
        from google.oauth2.credentials import Credentials
        from google_auth_oauthlib.flow import Flow
        
        flow = Flow.from_client_config(
            {
                "installed": {
                    "client_id": client_id,
                    "client_secret": client_secret,
                    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                    "token_uri": "https://oauth2.googleapis.com/token",
                    "redirect_uris": ["http://localhost"]
                }
            },
            scopes=SCOPES
        )
        flow.redirect_uri = 'http://localhost:8080'
        
        print("=" * 70)
        print("🔐 YouTube OAuth2 인증 시작")
        print("=" * 70)
        print("\n1. 브라우저가 자동으로 열립니다.")
        print("2. Google 계정으로 로그인")
        print("3. YouTube 업로드 권한 승인")
        print("\n진행 중...\n")
        
        creds = flow.run_local_server(port=8080)
        
        print("\n" + "=" * 70)
        print("✅ 토큰 획득 완료!")
        print("=" * 70)
        print(f"\n📋 Railway 환경 변수 설정:")
        print(f"YOUTUBE_CLIENT_ID={client_id}")
        print(f"YOUTUBE_CLIENT_SECRET={client_secret}")
        print(f"YOUTUBE_ACCESS_TOKEN={creds.token}")
        print(f"YOUTUBE_REFRESH_TOKEN={creds.refresh_token}")
        print("\n💾 토큰을 ~/.youtube_token.pickle에 저장했습니다.")
        print("=" * 70)
        
        # 토큰 저장
        token_file = os.path.expanduser('~/.youtube_token.pickle')
        with open(token_file, 'wb') as token:
            pickle.dump(creds, token)
        
        return creds
    
    # 파일 기반 인증
    credentials_file = os.path.expanduser('~/.youtube_credentials.json')
    
    if not os.path.exists(credentials_file):
        print("=" * 70)
        print("❌ OAuth2 클라이언트 정보가 없습니다.")
        print("=" * 70)
        print("\n📋 설정 방법:")
        print("1. Google Cloud Console 접속:")
        print("   https://console.cloud.google.com/apis/credentials")
        print("2. OAuth2 클라이언트 ID 생성")
        print("3. 클라이언트 ID를 다운로드하여 다음 경로에 저장:")
        print(f"   {credentials_file}")
        print("\n또는 환경 변수 설정:")
        print("   export YOUTUBE_CLIENT_ID=...")
        print("   export YOUTUBE_CLIENT_SECRET=...")
        print("=" * 70)
        return None
    
    flow = InstalledAppFlow.from_client_secrets_file(
        credentials_file, SCOPES)
    
    print("=" * 70)
    print("🔐 YouTube OAuth2 인증 시작")
    print("=" * 70)
    print("\n1. 브라우저가 자동으로 열립니다.")
    print("2. Google 계정으로 로그인")
    print("3. YouTube 업로드 권한 승인")
    print("\n진행 중...\n")
    
    creds = flow.run_local_server(port=0)
    
    print("\n" + "=" * 70)
    print("✅ 토큰 획득 완료!")
    print("=" * 70)
    print(f"\n📋 Railway 환경 변수 설정:")
    print(f"YOUTUBE_ACCESS_TOKEN={creds.token}")
    print(f"YOUTUBE_REFRESH_TOKEN={creds.refresh_token}")
    print("\n💾 토큰을 ~/.youtube_token.pickle에 저장했습니다.")
    print("=" * 70)
    
    # 토큰 저장
    token_file = os.path.expanduser('~/.youtube_token.pickle')
    with open(token_file, 'wb') as token:
        pickle.dump(creds, token)
    
    return creds

if __name__ == '__main__':
    get_youtube_tokens()
