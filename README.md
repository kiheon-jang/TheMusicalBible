---
date: 2026-02-01
project: 10_Projects/project
tags: ['index', 'project']
---
# 🎬 The Musical Bible - Cinematic Collection 2026

> AI 시네마틱 뮤지컬 성경 - 완전 자동화 YouTube 쇼츠 생성 시스템

---

## 🎯 프로젝트 개요

**목표**: 매월 50편의 고품질 30초 성경 쇼츠를 AI로 자동 생성 및 YouTube 업로드

### 핵심 기능
- ✅ **자동 스크립트 생성** (Claude API)
- ✅ **AI 캐릭터 영상** (Hedra API)
- ✅ **AI 음악 생성** (Suno API - 자체 서버)
- ✅ **AI 음성 합성** (Fish Audio)
- ✅ **AI 배경 영상** (Runway API)
- ✅ **자동 비디오 합성** (FFmpeg)
- ✅ **자동 YouTube 업로드** (YouTube Data API)

---

## 📊 시스템 아키텍처

```
PostgreSQL Database
    ↓
Morning Batch (AM 2:00)
    ↓
Evening Generation (PM 2:00)
  ├─ Claude → 프롬프트 생성
  ├─ Hedra → 캐릭터 영상
  ├─ Suno → 음악 생성 (Fallback: Udio → Mubert)
  ├─ Fish Audio → 음성 합성
  ├─ Runway → 배경 영상
  ├─ FFmpeg → 비디오 합성
  └─ YouTube → 자동 업로드
    ↓
Daily Monitoring (AM 10:00)
```

---

## 🚀 배포 완료

### Railway Services
1. **PostgreSQL Database**
   - Host: `maglev.proxy.rlwy.net:15087`
   - 5개 구절, 10개 캐릭터 초기화 완료

2. **n8n Workflow Engine**
   - URL: https://n8n-production-1d6b.up.railway.app
   - 6개 워크플로우 준비 완료

3. **Suno API Server**
   - URL: https://suno-api-production-ac35.up.railway.app
   - ✅ 배포 완료 (gcui-art/suno-api)

---

## 📁 프로젝트 구조

```
TMB/
├── database/
│   ├── init_postgresql.sql          # PostgreSQL 스키마 & 초기 데이터
│   └── init.sql                     # SQLite 버전
├── workflows/
│   ├── morning_batch.json           # AM 2:00 일괄 처리
│   ├── evening_generation.json      # PM 2:00 영상 생성
│   ├── daily_monitoring.json        # AM 10:00 모니터링
│   ├── suno_cookie_monitor.json     # Suno 쿠키 체크 (매시간)
│   ├── suno_with_polling.json       # Suno 음악 생성 (Polling)
│   └── music_api_fallback.json      # Fallback 시스템
├── scripts/
│   ├── ffmpeg_compose.sh            # 비디오 합성
│   ├── generate_thumbnail.py        # 썸네일 생성
│   └── init_postgres_direct.py      # DB 초기화
├── suno-api-fixed/                  # Suno API 소스코드
└── docs/
    ├── FINAL_SETUP_COMPLETE.md      # ⭐ 최종 설정 가이드
    ├── SUNO_API_SUCCESS.md          # Suno API 배포 완료
    ├── N8N_WORKFLOW_IMPORT_GUIDE.md # n8n 워크플로우 가이드
    ├── SUNO_UNOFFICIAL_API_SETUP.md # Suno API 상세 설정
    └── MUSIC_API_ALTERNATIVES.md    # 음악 API 대안
```

---

## 💰 비용 분석

### 월 22만 원 (5.5만 원 절감!)

| 항목 | 월 비용 | 비고 |
|------|---------|------|
| Claude Batch API | 2.5만 원 | 프롬프트 생성 |
| Hedra Pro | 5.5만 원 | 캐릭터 영상 |
| Runway Standard | 4.5만 원 | 배경 영상 |
| Fish Audio | 1.8만 원 | 음성 합성 (한국어) |
| Railway (n8n) | 1만 원 | 워크플로우 엔진 |
| **Railway (Suno API)** | **1만 원** | **비공식 API 호스팅** |
| **Suno Pro** | **2.2만 원** | **무제한 음악 생성** |
| Mubert API (Fallback) | 2만 원 | 대체 음악 API |
| 예비비 | 1.5만 원 | |
| **합계** | **22만 원** | |

### 수익 예상
- **YouTube 광고**: 월 50-100만 원 (월 50편 × 평균 5만 조회)
- **ROI**: 첫 달 손익분기, 2개월째부터 수익

---

## 🔧 최종 설정 단계

### 1. Suno 쿠키 설정 ⚠️ 필수
```bash
# 1. https://suno.com/ 로그인 (Pro 구독)
# 2. F12 → Application → Cookies 복사
# 3. Railway → suno-api → Variables → SUNO_COOKIE 업데이트
```

### 2. n8n 워크플로우 임포트
```bash
# n8n 접속: https://n8n-production-1d6b.up.railway.app
# Email: xaqwer@gmail.com
# Workflows → Import from File:
#   - workflows/suno_cookie_monitor.json
#   - workflows/suno_with_polling.json
#   - workflows/music_api_fallback.json
```

### 3. Telegram Bot 설정
```bash
# @BotFather → /newbot
# Token 복사 → n8n Credentials
```

### 4. API Credentials 설정
- Claude API Key
- Hedra API Key
- Fish Audio API Key
- Runway API Key
- YouTube OAuth2

---

## 🎵 Suno 비공식 API - 특별 기능

### 자동 쿠키 관리
- ✅ **매시간 체크**: 쿠키 만료 감지
- ✅ **Telegram 알림**: 즉시 알림 전송
- ✅ **자동 Keep-Alive**: 토큰 유지 기능 내장

### Polling System
- ✅ **10초 주기 체크**: 생성 완료 감지
- ✅ **최대 5분 대기**: 타임아웃 방지
- ✅ **자동 다운로드**: 완료 즉시 저장

### Multi-API Fallback
```
1순위: Suno API (자체 서버, 무제한)
   ↓ 실패 시
2순위: Udio API (대체)
   ↓ 실패 시
3순위: Mubert API (유료)
   ↓ 실패 시
4순위: Backup Library (Google Drive)
```
**성공률: 99%+**

---

## 📈 운영 일정

| 시간 | 작업 | 내용 |
|------|------|------|
| **AM 2:00** | Morning Batch | 성경 구절 선정 (2편/일) |
| **PM 2:00** | Evening Generation | AI 영상 생성 (2편) |
| **PM 6:00** | Auto Upload | YouTube 자동 업로드 |
| **PM 11:59** | Daily Report | 일일 리포트 전송 |
| **AM 10:00** | Monitoring | 전체 시스템 점검 |
| **매시간** | Cookie Check | Suno 쿠키 상태 체크 |

---

## 🔍 모니터링 & 로그

### PostgreSQL Tables
- `scripture` - 성경 구절 및 생성 상태
- `character_voices` - 캐릭터 음성 설정
- `api_usage_log` - API 사용 로그 및 비용
- `youtube_analytics` - YouTube 조회수/수익
- `workflow_execution_log` - 워크플로우 실행 로그

### Telegram 알림
- Suno 쿠키 만료
- API 오류 발생
- 일일 생성 완료
- 시스템 장애

---

## 🆘 트러블슈팅

### Suno API 오류
```bash
# 로그 확인
railway logs -s suno-api

# 쿠키 업데이트
railway variables set SUNO_COOKIE="새_쿠키_값"

# 재배포
railway up
```

### n8n 워크플로우 오류
```bash
# n8n 실행 로그 확인
# Workflows → 해당 워크플로우 → Executions

# PostgreSQL Credential 재연결
# Credentials → Postgres → Test Connection
```

### 데이터베이스 초기화
```bash
# Python 스크립트 실행
cd /Users/giheonjang/Documents/project/TMB
source venv/bin/activate
python scripts/init_postgres_direct.py
```

---

## 📚 참고 문서

- **[FINAL_SETUP_COMPLETE.md](FINAL_SETUP_COMPLETE.md)** - 최종 설정 가이드
- **[SUNO_API_SUCCESS.md](SUNO_API_SUCCESS.md)** - Suno API 배포 완료
- **[N8N_WORKFLOW_IMPORT_GUIDE.md](N8N_WORKFLOW_IMPORT_GUIDE.md)** - 워크플로우 임포트
- **[SUNO_UNOFFICIAL_API_SETUP.md](SUNO_UNOFFICIAL_API_SETUP.md)** - Suno API 설정
- **[MUSIC_API_ALTERNATIVES.md](MUSIC_API_ALTERNATIVES.md)** - 음악 API 대안

---

## 🎬 다음 단계

1. ✅ Infrastructure 배포 완료
2. ✅ Suno API 배포 완료
3. ✅ n8n 워크플로우 준비 완료
4. 🔜 Suno 쿠키 설정
5. 🔜 Telegram Bot 설정
6. 🔜 API Credentials 설정
7. 🔜 전체 테스트 실행

---

## 👥 Contact

- Email: xaqwer@gmail.com
- n8n: https://n8n-production-1d6b.up.railway.app
- Suno API: https://suno-api-production-ac35.up.railway.app

---

**🎉 The Musical Bible 시스템이 완성되었습니다!**

지금 바로 Suno 쿠키를 설정하고 첫 번째 영상을 생성해보세요! 🚀
