---
date: 2026-02-01
project: 10_Projects/project
tags: ['project']
---
# YouTube OAuth2 설정 가이드

## 🎯 목표
YouTube API를 사용하여 영상을 자동 업로드하기 위한 OAuth2 토큰 획득

---

## 📋 1단계: Python 패키지 설치

```bash
pip3 install google-api-python-client google-auth-oauthlib google-auth-httplib2
```

---

## 📋 2단계: OAuth2 토큰 획득

### 방법 A: 환경 변수 사용 (권장)

```bash
# 환경 변수 설정
export YOUTUBE_CLIENT_ID="1053902423625-6dlr4lgb58e20d0nteaq16ufrnaj7hq0.apps.googleusercontent.com"
export YOUTUBE_CLIENT_SECRET="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"

# 토큰 획득 스크립트 실행
python3 scripts/get_youtube_token.py
```

### 방법 B: 파일 사용

1. Google Cloud Console에서 OAuth2 클라이언트 ID 다운로드
2. `~/.youtube_credentials.json`에 저장
3. 스크립트 실행:
   ```bash
   python3 scripts/get_youtube_token.py
   ```

---

## 📋 3단계: Railway 환경 변수 설정

토큰 획득 후, Railway n8n 서비스에 다음 환경 변수를 추가:

```
YOUTUBE_CLIENT_ID=1053902423625-6dlr4lgb58e20d0nteaq16ufrnaj7hq0.apps.googleusercontent.com
YOUTUBE_CLIENT_SECRET=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
YOUTUBE_ACCESS_TOKEN=<스크립트에서 출력된 값>
YOUTUBE_REFRESH_TOKEN=<스크립트에서 출력된 값>
```

---

## ✅ 확인

스크립트 실행 후 다음과 같은 출력이 나옵니다:

```
======================================================================
✅ 토큰 획득 완료!
======================================================================

📋 Railway 환경 변수 설정:
YOUTUBE_CLIENT_ID=...
YOUTUBE_CLIENT_SECRET=...
YOUTUBE_ACCESS_TOKEN=...
YOUTUBE_REFRESH_TOKEN=...
```

이 값들을 Railway 환경 변수로 설정하면 됩니다.

---

## 🔄 토큰 갱신

Access Token은 만료되지만, Refresh Token이 있으면 자동으로 갱신됩니다.
`upload_youtube.py` 스크립트가 자동으로 처리합니다.

---

## ⚠️ 주의사항

- Refresh Token은 안전하게 보관하세요
- 환경 변수는 Railway에서만 설정하고, 코드에는 포함하지 마세요
- 토큰이 만료되면 다시 `get_youtube_token.py`를 실행하세요
