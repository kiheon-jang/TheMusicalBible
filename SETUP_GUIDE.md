# The Musical Bible (TMB) - 설정 가이드

이 가이드는 Railway에 n8n을 배포하고 The Musical Bible 시스템을 완전히 설정하는 방법을 설명합니다.

## 목차

1. [Railway 프로젝트 생성](#1-railway-프로젝트-생성)
2. [n8n 배포](#2-n8n-배포)
3. [데이터베이스 초기화](#3-데이터베이스-초기화)
4. [API Credentials 설정](#4-api-credentials-설정)
5. [워크플로우 임포트](#5-워크플로우-임포트)
6. [테스트 실행](#6-테스트-실행)

---

## 1. Railway 프로젝트 생성

### 1.1 Railway 가입 및 로그인

1. https://railway.app 접속
2. GitHub 계정으로 로그인
3. 대시보드로 이동

### 1.2 새 프로젝트 생성

1. **New Project** 클릭
2. **Deploy from GitHub repo** 선택
3. 이 저장소를 선택하거나 **Empty Project** 선택

### 1.3 서비스 추가

1. 프로젝트 내에서 **+ New** 클릭
2. **GitHub Repo** 또는 **Docker** 선택
3. Docker Image: `n8n/n8n:latest` 입력

---

## 2. n8n 배포

### 2.1 Dockerfile 사용 (권장)

이 저장소의 `Dockerfile`을 사용하면 FFmpeg, Python, SQLite가 모두 포함된 n8n이 배포됩니다.

1. Railway 대시보드에서 서비스 선택
2. **Settings** → **Source** → **Dockerfile Path**: `Dockerfile` 설정
3. **Deploy** 클릭

### 2.2 환경 변수 설정

Railway 대시보드에서 **Variables** 탭에 다음 환경 변수 추가:

```bash
# n8n 기본 설정
N8N_BASIC_AUTH_ACTIVE=true
N8N_BASIC_AUTH_USER=admin
N8N_BASIC_AUTH_PASSWORD=[강력한 비밀번호 설정]
N8N_HOST=0.0.0.0
N8N_PORT=5678
N8N_PROTOCOL=https

# 웹훅 URL (Railway가 자동 생성)
WEBHOOK_URL=https://n8n-production-1d6b.up.railway.app

# 데이터베이스 경로
DB_SQLITE_PATH=/data/database/scripture.db

# Google Sheets (선택사항)
GOOGLE_SHEETS_DOCUMENT_ID=[Google Sheets 문서 ID]
```

### 2.3 볼륨 마운트 (데이터 영구 저장)

1. **Settings** → **Volumes** → **+ New Volume**
2. Mount Path: `/data`
3. 이렇게 하면 데이터베이스와 출력 파일이 영구 저장됩니다.

### 2.4 n8n 접속 확인

1. Railway 대시보드에서 **Settings** → **Domains** 확인
2. 생성된 URL로 접속 (예: `https://n8n-production-1d6b.up.railway.app`)
3. 초기 관리자 계정 생성

---

## 3. 데이터베이스 초기화

### 3.1 Railway 터미널 접속

1. Railway 대시보드에서 서비스 선택
2. **Deployments** → **View Logs** → **Shell** 탭 클릭
3. 또는 **Settings** → **Connect** → **Railway CLI** 사용

### 3.2 SQLite 데이터베이스 생성

```bash
# 데이터베이스 디렉토리 생성
mkdir -p /data/database

# 스키마 생성
sqlite3 /data/database/scripture.db < /data/database/init.sql

# 샘플 데이터 입력
sqlite3 /data/database/scripture.db < /data/database/seed_data.sql

# 확인
sqlite3 /data/database/scripture.db "SELECT COUNT(*) FROM scripture;"
```

### 3.3 n8n에서 SQLite 연결 테스트

1. n8n 대시보드 접속
2. **Credentials** → **+ Add Credential** → **SQLite**
3. Database Path: `/data/database/scripture.db`
4. **Test** 클릭하여 연결 확인

---

## 4. API Credentials 설정

n8n 대시보드에서 각 API의 Credential을 추가합니다.

### 4.1 Claude API

1. **Credentials** → **+ Add Credential** → **HTTP Header Auth**
2. Name: `Claude API`
3. Header Name: `x-api-key`
4. Header Value: `sk-ant-...` (Anthropic API 키)
5. 또는 **HTTP Request** 노드에서 직접 설정

**참고**: Claude API는 HTTP Request 노드에서 다음과 같이 설정:
- URL: `https://api.anthropic.com/v1/messages`
- Authentication: `Header Auth`
- Headers:
  - `anthropic-version: 2023-06-01`
  - `x-api-key: [API 키]`

### 4.2 Hedra AI

1. **Credentials** → **+ Add Credential** → **HTTP Header Auth**
2. Name: `Hedra API`
3. Header Name: `Authorization`
4. Header Value: `Bearer hedra-...` (Hedra API 키)

### 4.3 Suno API

1. **Credentials** → **+ Add Credential** → **HTTP Header Auth**
2. Name: `Suno API`
3. Header Name: `Authorization`
4. Header Value: `Bearer suno-...` (Suno API 키)

### 4.4 Fish Audio

1. **Credentials** → **+ Add Credential** → **HTTP Header Auth**
2. Name: `Fish Audio API`
3. Header Name: `Authorization`
4. Header Value: `Bearer fish-...` (Fish Audio API 키)

### 4.5 Runway

1. **Credentials** → **+ Add Credential** → **HTTP Header Auth`
2. Name: `Runway API`
3. Header Name: `Authorization`
4. Header Value: `Bearer runway-...` (Runway API 키)

### 4.6 YouTube API

1. Google Cloud Console에서 프로젝트 생성
2. YouTube Data API v3 활성화
3. OAuth 2.0 클라이언트 ID 생성
4. n8n에서 **Credentials** → **+ Add Credential** → **YouTube OAuth2 API**
5. Client ID, Client Secret 입력
6. **Connect my account** 클릭하여 권한 부여

### 4.7 Google Sheets API

1. Google Cloud Console에서 Sheets API 활성화
2. n8n에서 **Credentials** → **+ Add Credential** → **Google Sheets OAuth2 API**
3. Client ID, Client Secret 입력
4. **Connect my account** 클릭하여 권한 부여

---

## 5. 워크플로우 임포트

### 5.1 워크플로우 파일 준비

이 저장소의 `workflows/` 디렉토리에 다음 파일들이 있습니다:
- `morning_batch.json`
- `evening_generation.json`
- `daily_monitoring.json`

### 5.2 n8n에서 임포트

1. n8n 대시보드 접속
2. **Workflows** → **+ Add Workflow** → **Import from File**
3. 각 JSON 파일을 순서대로 임포트:
   - `morning_batch.json`
   - `evening_generation.json`
   - `daily_monitoring.json`

### 5.3 Credentials 연결

각 워크플로우의 노드에서 Credentials를 연결합니다:

1. 워크플로우 편집 모드 진입
2. 각 API 노드 클릭
3. **Credentials** 드롭다운에서 위에서 생성한 Credential 선택
4. **Save** 클릭

### 5.4 SQLite 경로 확인

SQLite 노드에서 Database Path가 `/data/database/scripture.db`로 설정되어 있는지 확인합니다.

---

## 6. 테스트 실행

### 6.1 Morning Batch 워크플로우 테스트

1. `morning_batch.json` 워크플로우 열기
2. **Execute Workflow** 클릭
3. 로그 확인:
   - SQLite에서 구절 3개 불러오기 성공
   - Claude API 호출 성공
   - SQLite 업데이트 성공

### 6.2 Evening Generation 워크플로우 테스트

**주의**: 이 워크플로우는 실제 API 호출을 하므로 비용이 발생합니다.

1. `evening_generation.json` 워크플로우 열기
2. **Execute Workflow** 클릭
3. 각 API 노드의 응답 확인:
   - Suno: 음악 URL
   - Fish Audio: 음성 URL
   - Hedra: 영상 URL
   - Runway: 배경 영상 URL (선택)
4. FFmpeg 합성 확인
5. 썸네일 생성 확인
6. YouTube 업로드 확인 (테스트 시에는 `privacyStatus: unlisted` 권장)

### 6.3 Daily Monitoring 워크플로우 테스트

1. `daily_monitoring.json` 워크플로우 열기
2. **Execute Workflow** 클릭
3. YouTube Analytics 데이터 수집 확인
4. SQLite 업데이트 확인
5. Google Sheets 기록 확인

---

## 7. 자동화 활성화

### 7.1 워크플로우 활성화

각 워크플로우의 Settings에서:
1. **Active** 토글을 **ON**으로 설정
2. Cron Expression 확인:
   - Morning Batch: `0 2 * * *` (매일 AM 2:00)
   - Evening Generation: `0 14 * * *` (매일 PM 2:00)
   - Daily Monitoring: `0 10 * * *` (매일 AM 10:00)

### 7.2 모니터링

1. Railway 대시보드에서 로그 확인
2. n8n 대시보드에서 실행 이력 확인
3. Google Sheets에서 통계 확인

---

## 8. 문제 해결

### 8.1 n8n 접속 불가

- Railway 대시보드에서 서비스 로그 확인
- 환경 변수 `N8N_HOST=0.0.0.0` 확인
- 포트 `5678` 확인

### 8.2 SQLite 오류

- 데이터베이스 파일 경로 확인: `/data/database/scripture.db`
- 파일 권한 확인: `chmod 666 /data/database/scripture.db`
- 볼륨 마운트 확인

### 8.3 API 호출 실패

- Credentials에서 API 키 확인
- Rate Limit 확인 (각 API별 제한)
- 네트워크 연결 확인

### 8.4 FFmpeg 오류

- Railway 터미널에서 `ffmpeg -version` 확인
- Dockerfile에 FFmpeg 설치 확인
- 스크립트 실행 권한 확인: `chmod +x /data/scripts/ffmpeg_compose.sh`

### 8.5 Python 스크립트 오류

- Python 버전 확인: `python3 --version`
- Pillow 설치 확인: `pip3 list | grep Pillow`
- 스크립트 실행 권한 확인: `chmod +x /data/scripts/generate_thumbnail.py`

---

## 9. 다음 단계

1. **성경 데이터 확장**: `seed_data.sql`에 더 많은 구절 추가
2. **캐릭터 Identity Anchor 이미지 생성**: DALL-E 3로 각 캐릭터 이미지 생성
3. **음성 품질 최적화**: Fish Audio에서 각 캐릭터별 음성 테스트
4. **YouTube 채널 설정**: 채널 설명, 썸네일 템플릿, 플레이리스트 생성
5. **모니터링 대시보드**: Google Sheets 또는 다른 도구로 통계 시각화

---

## 10. 지원

문제가 발생하면:
1. Railway 로그 확인
2. n8n 실행 이력 확인
3. SQLite 데이터베이스 직접 조회
4. 각 API 문서 참조

**성공적인 배포를 기원합니다!** 🎬✨
