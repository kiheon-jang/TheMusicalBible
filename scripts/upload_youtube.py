#!/usr/bin/env python3
"""
YouTube Data API v3를 사용한 영상 업로드 스크립트
The Musical Bible (TMB)
"""
import sys
import json
import os
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle

# YouTube API 스코프
SCOPES = ['https://www.googleapis.com/auth/youtube.upload']

def get_authenticated_service():
    """OAuth2 인증을 통해 YouTube API 서비스 객체 반환"""
    creds = None
    
    # 환경 변수에서 토큰 확인 (Railway/n8n에서 사용)
    access_token = os.environ.get('YOUTUBE_ACCESS_TOKEN')
    client_id = os.environ.get('YOUTUBE_CLIENT_ID')
    client_secret = os.environ.get('YOUTUBE_CLIENT_SECRET')
    refresh_token = os.environ.get('YOUTUBE_REFRESH_TOKEN')
    
    if access_token and client_id and client_secret:
        from google.oauth2.credentials import Credentials as OAuth2Credentials
        creds = OAuth2Credentials(
            token=access_token,
            refresh_token=refresh_token,
            token_uri='https://oauth2.googleapis.com/token',
            client_id=client_id,
            client_secret=client_secret,
            scopes=SCOPES
        )
        # 토큰이 만료된 경우 자동 갱신
        if creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
                print("✅ OAuth2 토큰 자동 갱신 완료")
            except Exception as e:
                print(f"⚠️  토큰 갱신 실패: {e}")
                print("YOUTUBE_REFRESH_TOKEN을 확인하세요.")
                sys.exit(1)
        return build('youtube', 'v3', credentials=creds)
    
    # 로컬 환경: 파일 기반 인증
    token_file = os.path.expanduser('~/.youtube_token.pickle')
    credentials_file = os.path.expanduser('~/.youtube_credentials.json')
    
    # 저장된 토큰 로드
    if os.path.exists(token_file):
        with open(token_file, 'rb') as token:
            creds = pickle.load(token)
    
    # 토큰이 없거나 만료된 경우
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists(credentials_file):
                print("=" * 70)
                print("❌ YouTube OAuth2 인증 정보가 없습니다.")
                print("=" * 70)
                print("\n📋 해결 방법:")
                print("1. 환경 변수 설정 (Railway 권장):")
                print("   YOUTUBE_CLIENT_ID=...")
                print("   YOUTUBE_CLIENT_SECRET=...")
                print("   YOUTUBE_ACCESS_TOKEN=...")
                print("   YOUTUBE_REFRESH_TOKEN=...")
                print("\n2. 또는 로컬 파일 설정:")
                print("   ~/.youtube_credentials.json 파일 생성")
                print("   Google Cloud Console에서 OAuth2 클라이언트 ID 다운로드")
                print("=" * 70)
                sys.exit(1)
            
            flow = InstalledAppFlow.from_client_secrets_file(
                credentials_file, SCOPES)
            creds = flow.run_local_server(port=0)
        
        # 토큰 저장
        with open(token_file, 'wb') as token:
            pickle.dump(creds, token)
    
    return build('youtube', 'v3', credentials=creds)

def upload_video(video_path, thumbnail_path, title, description, response_file):
    """YouTube에 영상 업로드"""
    try:
        youtube = get_authenticated_service()
        
        # 메타데이터 설정
        body = {
            'snippet': {
                'title': title,
                'description': description,
                'tags': ['성경', '뮤지컬', 'AI', '영화'],
                'categoryId': '24'
            },
            'status': {
                'privacyStatus': 'public'
            }
        }
        
        # 영상 파일 업로드
        media = MediaFileUpload(video_path, chunksize=-1, resumable=True)
        
        insert_request = youtube.videos().insert(
            part=','.join(body.keys()),
            body=body,
            media_body=media
        )
        
        # 업로드 실행
        response = None
        while response is None:
            status, response = insert_request.next_chunk()
            if status:
                print(f"업로드 진행률: {int(status.progress() * 100)}%")
        
        # 썸네일 업로드 (선택사항)
        if os.path.exists(thumbnail_path):
            try:
                youtube.thumbnails().set(
                    videoId=response['id'],
                    media_body=MediaFileUpload(thumbnail_path)
                ).execute()
                print(f"썸네일 업로드 완료")
            except Exception as e:
                print(f"썸네일 업로드 실패 (무시): {e}")
        
        # 응답 저장
        with open(response_file, 'w', encoding='utf-8') as f:
            json.dump(response, f, ensure_ascii=False, indent=2)
        
        print(f"업로드 완료: https://www.youtube.com/watch?v={response['id']}")
        return response
        
    except Exception as e:
        error_response = {
            'error': str(e),
            'video_id': '',
            'url': ''
        }
        with open(response_file, 'w', encoding='utf-8') as f:
            json.dump(error_response, f, ensure_ascii=False, indent=2)
        print(f"ERROR: {e}")
        sys.exit(1)

if __name__ == '__main__':
    if len(sys.argv) < 6:
        print("Usage: upload_youtube.py <video_path> <thumbnail_path> <title> <description> <response_file>")
        sys.exit(1)
    
    video_path = sys.argv[1]
    thumbnail_path = sys.argv[2]
    title = sys.argv[3]
    description = sys.argv[4]
    response_file = sys.argv[5]
    
    if not os.path.exists(video_path):
        print(f"ERROR: 영상 파일이 없습니다: {video_path}")
        sys.exit(1)
    
    upload_video(video_path, thumbnail_path, title, description, response_file)
