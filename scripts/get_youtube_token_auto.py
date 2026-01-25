#!/usr/bin/env python3
"""
YouTube OAuth2 토큰 자동 획득 스크립트 (Playwright 사용)
"""
import os
import sys
import json
import time
from urllib.parse import urlparse, parse_qs
from playwright.sync_api import sync_playwright

# YouTube API 스코프
SCOPES = ['https://www.googleapis.com/auth/youtube.upload']

def get_youtube_tokens_auto(email=None, password=None):
    """Playwright를 사용하여 OAuth2 토큰 자동 획득"""
    
    client_id = os.environ.get('YOUTUBE_CLIENT_ID')
    client_secret = os.environ.get('YOUTUBE_CLIENT_SECRET')
    
    if not client_id or not client_secret:
        print("❌ YOUTUBE_CLIENT_ID와 YOUTUBE_CLIENT_SECRET 환경 변수가 필요합니다.")
        sys.exit(1)
    
    # OAuth2 인증 URL 생성
    auth_url = (
        f"https://accounts.google.com/o/oauth2/auth?"
        f"client_id={client_id}&"
        f"redirect_uri=http://localhost:8080&"
        f"response_type=code&"
        f"scope={'+'.join(SCOPES)}&"
        f"access_type=offline&"
        f"prompt=consent"
    )
    
    print("=" * 70)
    print("🔐 YouTube OAuth2 자동 인증 시작")
    print("=" * 70)
    print(f"\n📧 Google 계정: {email or '자동 입력 필요'}")
    print("🌐 브라우저를 열어 인증을 진행합니다...\n")
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        
        try:
            # OAuth2 인증 페이지로 이동
            page.goto(auth_url)
            time.sleep(2)
            
            # 이메일 입력
            if email:
                print(f"📧 이메일 입력 중: {email}")
                page.fill('input[type="email"]', email)
                page.click('button:has-text("다음")')
                time.sleep(2)
            else:
                print("⚠️  이메일을 수동으로 입력해주세요...")
                input("이메일 입력 후 Enter를 누르세요...")
            
            # 비밀번호 입력
            if password:
                print("🔑 비밀번호 입력 중...")
                page.fill('input[type="password"]', password)
                page.click('button:has-text("다음")')
                time.sleep(3)
            else:
                print("⚠️  비밀번호를 수동으로 입력해주세요...")
                input("비밀번호 입력 후 Enter를 누르세요...")
            
            # 권한 승인 대기
            print("⏳ 권한 승인 대기 중...")
            time.sleep(3)
            
            # "허용" 또는 "Allow" 버튼 클릭
            try:
                allow_button = page.locator('button:has-text("허용"), button:has-text("Allow")').first
                if allow_button.is_visible():
                    allow_button.click()
                    time.sleep(2)
            except:
                pass
            
            # 리다이렉트 URL에서 authorization code 추출
            print("🔍 인증 코드 추출 중...")
            max_wait = 30
            start_time = time.time()
            
            while time.time() - start_time < max_wait:
                current_url = page.url
                if 'localhost:8080' in current_url or 'code=' in current_url:
                    parsed = urlparse(current_url)
                    params = parse_qs(parsed.query)
                    if 'code' in params:
                        auth_code = params['code'][0]
                        print(f"✅ 인증 코드 획득: {auth_code[:20]}...")
                        break
                time.sleep(1)
            else:
                print("❌ 타임아웃: 인증 코드를 받지 못했습니다.")
                print(f"현재 URL: {page.url}")
                browser.close()
                sys.exit(1)
            
            browser.close()
            
            # Authorization code를 Access Token으로 교환
            print("\n🔄 Access Token 교환 중...")
            import requests
            
            token_url = "https://oauth2.googleapis.com/token"
            token_data = {
                'code': auth_code,
                'client_id': client_id,
                'client_secret': client_secret,
                'redirect_uri': 'http://localhost:8080',
                'grant_type': 'authorization_code'
            }
            
            response = requests.post(token_url, data=token_data)
            
            if response.status_code != 200:
                print(f"❌ 토큰 교환 실패: {response.text}")
                sys.exit(1)
            
            token_info = response.json()
            access_token = token_info.get('access_token')
            refresh_token = token_info.get('refresh_token')
            
            if not access_token:
                print(f"❌ Access Token 획득 실패: {token_info}")
                sys.exit(1)
            
            print("\n" + "=" * 70)
            print("✅ 토큰 획득 완료!")
            print("=" * 70)
            print(f"\n📋 Railway 환경 변수 설정:")
            print(f"YOUTUBE_CLIENT_ID={client_id}")
            print(f"YOUTUBE_CLIENT_SECRET={client_secret}")
            print(f"YOUTUBE_ACCESS_TOKEN={access_token}")
            if refresh_token:
                print(f"YOUTUBE_REFRESH_TOKEN={refresh_token}")
            print("\n💾 토큰 정보를 ~/.youtube_tokens.json에 저장했습니다.")
            print("=" * 70)
            
            # 토큰 저장
            token_file = os.path.expanduser('~/.youtube_tokens.json')
            with open(token_file, 'w') as f:
                json.dump({
                    'access_token': access_token,
                    'refresh_token': refresh_token,
                    'client_id': client_id,
                    'client_secret': client_secret
                }, f, indent=2)
            
            return {
                'access_token': access_token,
                'refresh_token': refresh_token
            }
            
        except Exception as e:
            print(f"\n❌ 오류 발생: {e}")
            browser.close()
            sys.exit(1)

if __name__ == '__main__':
    email = os.environ.get('GOOGLE_EMAIL')
    password = os.environ.get('GOOGLE_PASSWORD')
    
    if not email:
        email = input("Google 이메일을 입력하세요: ").strip()
    
    if not password:
        import getpass
        password = getpass.getpass("Google 비밀번호를 입력하세요: ")
    
    get_youtube_tokens_auto(email, password)
