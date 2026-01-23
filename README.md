# The Musical Bible (TMB) - Cinematic Collection 2026

성경을 영화처럼 경험하게 하는 자동화 AI 뮤지컬 생성 시스템

## 프로젝트 개요

- **목표**: 월 50개의 고품질 30초 쇼츠 자동 생성 및 YouTube 자동 업로드
- **예산**: 월 27.5만 원
- **기술 스택**: n8n, Claude, Hedra Pro, Suno, Fish Audio, Runway, FFmpeg
- **인프라**: Railway.app (n8n 호스팅)

## 프로젝트 구조

```
TMB/
├── database/
│   ├── init.sql              # SQLite 초기 스키마
│   └── seed_data.sql         # 샘플 성경 데이터
├── workflows/
│   ├── morning_batch.json    # 워크플로우 1: Morning Batch
│   ├── evening_generation.json # 워크플로우 2: Evening Generation
│   └── daily_monitoring.json  # 워크플로우 3: Daily Monitoring
├── scripts/
│   ├── ffmpeg_compose.sh     # FFmpeg 영상 합성 스크립트
│   └── generate_thumbnail.py # 썸네일 생성 스크립트
├── railway.json              # Railway 배포 설정
└── README.md
```

## 빠른 시작

### 1. Railway에 n8n 배포

```bash
# Railway CLI 설치 (선택사항)
npm i -g @railway/cli

# Railway 로그인
railway login

# 프로젝트 생성 및 배포
railway init
railway up
```

또는 Railway 웹 대시보드에서:
1. New Project → Deploy from GitHub
2. Docker Image: `n8n/n8n:latest`
3. Environment Variables 설정 (아래 참조)

### 2. n8n 환경 변수 설정

Railway 대시보드에서 다음 환경 변수 설정:

```
N8N_BASIC_AUTH_ACTIVE=true
N8N_BASIC_AUTH_USER=admin
N8N_BASIC_AUTH_PASSWORD=[비밀번호]
N8N_HOST=0.0.0.0
N8N_PORT=5678
N8N_PROTOCOL=https
WEBHOOK_URL=https://n8n-production-1d6b.up.railway.app
```

### 3. n8n Credentials 설정

n8n 대시보드 접속 후 Credentials 메뉴에서 다음 API 키 추가:

- **Claude API**: HTTP Request (API Key)
- **Hedra AI**: HTTP Request (API Key)
- **Suno API**: HTTP Request (API Key)
- **Fish Audio**: HTTP Request (API Key)
- **Runway**: HTTP Request (API Key)
- **YouTube**: OAuth2
- **Google Sheets**: OAuth2

### 4. 데이터베이스 초기화

```bash
# SQLite 데이터베이스 생성
sqlite3 database/scripture.db < database/init.sql

# 샘플 데이터 입력
sqlite3 database/scripture.db < database/seed_data.sql
```

### 5. 워크플로우 임포트

n8n 대시보드에서:
1. Workflows → Import from File
2. `workflows/morning_batch.json` 임포트
3. `workflows/evening_generation.json` 임포트
4. `workflows/daily_monitoring.json` 임포트

### 6. 워크플로우 활성화

각 워크플로우의 Settings에서:
- Active: ON
- Schedule 설정 확인

## 워크플로우 설명

### 워크플로우 1: Morning Batch (AM 2:00)

**목적**: 하루치 프롬프트 사전 생성

**프로세스**:
1. Cron Trigger (매일 AM 2:00)
2. SQLite에서 구절 3개 불러오기
3. Claude Batch API에 일괄 요청
4. batch_request_id 저장 및 대기

### 워크플로우 2: Evening Generation (PM 2:00)

**목적**: 실제 콘텐츠 생성 및 YouTube 업로드

**프로세스**:
1. Cron Trigger (매일 PM 2:00)
2. Claude Batch 결과 조회
3. 4개 API 병렬 실행 (Suno, Fish Audio, Hedra, Runway)
4. FFmpeg로 30초 영상 합성
5. 썸네일 생성
6. YouTube 자동 업로드
7. Google Sheets 기록

### 워크플로우 3: Daily Monitoring (AM 10:00)

**목적**: YouTube 통계 수집 및 분석

**프로세스**:
1. Cron Trigger (매일 AM 10:00)
2. YouTube Analytics API 호출
3. Google Sheets에 통계 기록

## 비용 구조

| 항목 | 월 비용 | 역할 |
|------|--------|------|
| Claude 3.5 Sonnet | 2.5만 원 | 프롬프트 생성 |
| Hedra Pro | 5.5만 원 | 얼굴 + 립싱크 영상 |
| Runway Standard | 4.5만 원 | 배경 영상 |
| Suno Pro | 2.2만 원 | 배경음악 |
| Fish Audio | 1.8만 원 | 음성 합성 |
| Railway.app | 1만 원 | n8n 호스팅 |
| 예비비 | 9.5만 원 | 재시도/복구 |
| **합계** | **27.5만 원** | |

## 예상 수익

- **Month 1-2**: 거의 없음 (조회수 적음)
- **Month 3**: YouTube 파트너 조건 달성, 광고 활성화
- **Month 6**: 월 $150-200 (약 20-26만 원)
- **Month 12**: 누적 투자 회수 가능
- **Year 2**: 월 30-50만 원 순수익 예상

## 문제 해결

### n8n 접속 불가
- Railway 대시보드에서 서비스 로그 확인
- 환경 변수 `N8N_HOST=0.0.0.0` 확인

### API 호출 실패
- n8n Credentials에서 API 키 확인
- Rate Limit 확인 (각 API별 제한)

### FFmpeg 오류
- Railway에서 FFmpeg 설치 확인
- Dockerfile에 FFmpeg 추가 필요

## 라이선스

이 프로젝트는 개인 사용 목적으로 제작되었습니다.
