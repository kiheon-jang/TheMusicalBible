# The Musical Bible (TMB) - 빠른 시작 가이드

## 🚀 5분 안에 시작하기

### 1단계: Railway 확인 (1분)

현재 n8n URL: `https://n8n-production-1d6b.up.railway.app`

1. Railway 대시보드 접속: https://railway.app
2. 해당 프로젝트 확인
3. 서비스 상태가 **Running**인지 확인

### 2단계: n8n 접속 (1분)

1. `https://n8n-production-1d6b.up.railway.app` 접속
2. 로그인 (기존 계정 또는 새 계정 생성)

### 3단계: 데이터베이스 초기화 (2분)

Railway 터미널에서:

```bash
# 데이터베이스 생성
mkdir -p /data/database
sqlite3 /data/database/scripture.db < /data/database/init.sql
sqlite3 /data/database/scripture.db < /data/database/seed_data.sql
```

또는 n8n에서 SQLite 노드를 사용하여 직접 실행:

1. 새 워크플로우 생성
2. SQLite 노드 추가
3. Database Path: `/data/database/scripture.db`
4. Query: `CREATE TABLE IF NOT EXISTS scripture (...)` (init.sql 내용 복사)
5. 실행

### 4단계: API Credentials 설정 (1분)

n8n → **Credentials** → 각 API 추가:

- **Claude API**: HTTP Header Auth
  - Header: `x-api-key`
  - Value: `sk-ant-...`
- **Hedra API**: HTTP Header Auth
  - Header: `Authorization`
  - Value: `Bearer hedra-...`
- **Suno API**: HTTP Header Auth
  - Header: `Authorization`
  - Value: `Bearer suno-...`
- **Fish Audio**: HTTP Header Auth
  - Header: `Authorization`
  - Value: `Bearer fish-...`
- **Runway**: HTTP Header Auth
  - Header: `Authorization`
  - Value: `Bearer runway-...`
- **YouTube**: OAuth2 (Google Cloud Console에서 설정 필요)

### 5단계: 워크플로우 임포트

**방법 1: JSON 파일 임포트 (권장)**

1. n8n → **Workflows** → **Import from File**
2. `workflows/morning_batch.json` 선택
3. `workflows/evening_generation.json` 선택
4. `workflows/daily_monitoring.json` 선택

**방법 2: 수동 생성**

각 워크플로우를 `workflows/*.json` 파일을 참고하여 수동으로 생성합니다.

### 6단계: Credentials 연결

각 워크플로우에서:

1. SQLite 노드 → Credential 선택
2. 각 API 노드 → 해당 Credential 선택
3. **Save** 클릭

### 7단계: 테스트 실행

**Morning Batch 테스트:**

1. `morning_batch.json` 워크플로우 열기
2. **Execute Workflow** 클릭
3. 로그 확인:
   - ✅ SQLite에서 구절 3개 불러오기
   - ✅ Claude API 호출
   - ✅ SQLite 업데이트

**Evening Generation 테스트 (비용 발생 주의!):**

1. `evening_generation.json` 워크플로우 열기
2. **Execute Workflow** 클릭
3. 각 API 응답 확인
4. FFmpeg 합성 확인
5. YouTube 업로드 확인 (테스트 시 `unlisted` 권장)

### 8단계: 자동화 활성화

각 워크플로우 Settings에서:

- **Active**: ON
- **Schedule**:
  - Morning Batch: `0 2 * * *` (매일 AM 2:00)
  - Evening Generation: `0 14 * * *` (매일 PM 2:00)
  - Daily Monitoring: `0 10 * * *` (매일 AM 10:00)

## 📋 필수 확인사항

### Railway 환경 변수

```bash
N8N_BASIC_AUTH_ACTIVE=true
N8N_BASIC_AUTH_USER=admin
N8N_BASIC_AUTH_PASSWORD=[비밀번호]
N8N_HOST=0.0.0.0
N8N_PORT=5678
N8N_PROTOCOL=https
DB_SQLITE_PATH=/data/database/scripture.db
```

### 스크립트 경로

- FFmpeg: `/data/scripts/ffmpeg_compose.sh`
- Python: `/data/scripts/generate_thumbnail.py`
- 데이터베이스: `/data/database/scripture.db`

### 볼륨 마운트

Railway에서 `/data` 볼륨이 마운트되어 있어야 합니다.

## ⚠️ 주의사항

1. **비용**: Evening Generation은 실제 API 호출을 하므로 비용 발생
2. **Rate Limit**: 각 API별 월 제한 확인
3. **데이터 백업**: SQLite 정기 백업 필요
4. **보안**: API 키는 n8n Credentials에만 저장

## 🆘 문제 해결

### n8n 접속 불가
→ Railway 로그 확인, 환경 변수 확인

### SQLite 오류
→ 파일 경로 확인, 권한 확인

### API 호출 실패
→ Credentials 확인, Rate Limit 확인

### FFmpeg 오류
→ FFmpeg 설치 확인, 스크립트 권한 확인

## 📚 상세 가이드

- **SETUP_GUIDE.md**: 전체 설정 가이드
- **DEPLOYMENT_CHECKLIST.md**: 배포 체크리스트
- **README.md**: 프로젝트 개요

## 🎬 다음 단계

1. 성경 데이터 확장 (1,000개+ 구절)
2. 캐릭터 Identity Anchor 이미지 생성
3. YouTube 채널 설정
4. 모니터링 대시보드 구축

**성공적인 시작을 기원합니다!** ✨
