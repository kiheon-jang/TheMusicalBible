---
date: 2026-02-01
project: 10_Projects/project
tags: ['project']
---
# Railway + n8n 대신 더 단순한 자동화 솔루션

> 현재: Railway(PostgreSQL, n8n, Suno API) + n8n 워크플로우 25+ 노드로 전체 파이프라인 구동  
> 목표: 유지보수·디버깅이 쉬운 더 단순한 구조

---

## 1. 현재 구조가 복잡한 이유

| 요소 | 복잡도 |
|------|--------|
| **n8n** | Cron → Postgres → Code(JS) → Claude → 파싱 → Postgres → 분기 → Suno(폴링 루프) → Fish/Hedra/Runway 병렬 → Merge → FFmpeg/썸네일/YouTube → Postgres |
| **Credential** | PostgreSQL, Anthropic, Suno, Fish Audio, Hedra, Runway, YouTube OAuth 등 7개 이상 |
| **인프라** | Railway 프로젝트 3서비스(DB, n8n, Suno API) + n8n 워크플로우 6개 |
| **디버깅** | n8n 실행 로그·노드별 데이터 추적이 어렵고, JS 코드는 버전 관리가 n8n 내부에 묶임 |

---

## 2. 대안 요약

| 대안 | 복잡도 | 비용 | 추천도 | 한 줄 설명 |
|------|--------|------|--------|------------|
| **A. 오케스트레이터 API + 단순 트리거** | ⭐⭐ | 기존과 동일 | ⭐⭐⭐⭐⭐ | **가장 추천.** 비즈니스 로직은 하나의 API로, n8n은 “스케줄 + 1번 HTTP 호출”만 담당 |
| **B. 풀 Python/Node 파이프라인** | ⭐ | Railway 1서비스만 추가 | ⭐⭐⭐⭐ | n8n 제거. 스크립트 하나가 DB→Claude→…→YouTube까지 수행, Railway Cron 또는 GitHub Actions로 실행 |
| **C. GitHub Actions 스케줄** | ⭐ | 무료(공개) / 제한(비공개) | ⭐⭐⭐ | 워크플로우를 코드로 두고, cron으로 “파이프라인 API 호출” 또는 “스크립트 실행”만 수행 |
| **D. Inngest / Trigger.dev** | ⭐⭐ | 무료 티어 있음 | ⭐⭐⭐ | 코드 기반 워크플로우 + 스케줄/재시도. n8n 대체용 |
| **E. n8n 유지 + 노드 수만 축소** | ⭐⭐⭐ | 동일 | ⭐⭐ | “Cron → HTTP 1번”으로 줄이고, 나머지는 오케스트레이터 API에 위임 |

---

## 3. 추천: A. 오케스트레이터 API + 단순 트리거

### 아이디어

- **지금**: n8n이 “DB 조회 → Claude → Postgres 저장 → Suno/Fish/Hedra/Runway → Merge → FFmpeg → YouTube → Postgres” 전부 노드로 처리.
- **변경**: 이 흐름을 **한 서비스(오케스트레이터 API)** 에 넣고, n8n은 **“매일 AM 3:00에 이 API 한 번 호출”** 만 하도록 축소.

### 구조

```
[Railway Cron 또는 n8n 단일 워크플로우]
  └─ 매일 AM 3:00 → POST https://your-orchestrator.up.railway.app/run-daily
        ↓
[오케스트레이터 API (FastAPI/Flask)]
  ├─ PostgreSQL에서 pending 스토리 N개 조회
  ├─ 스토리별: Claude → 프롬프트 저장
  ├─ 스토리별: Suno / Fish / Hedra / Runway (병렬 또는 순차)
  ├─ FFmpeg 합성, 썸네일, YouTube 업로드
  └─ PostgreSQL 최종 업데이트
```

### 장점

- n8n: **Cron 노드 1개 + HTTP Request 노드 1개** 만 남기면 됨. Credential은 “오케스트레이터 URL” 하나만 필요할 수 있음.
- **비즈니스 로직은 전부 코드**에 있으므로 Git, 테스트, 로그가 쉬움.
- 기존 Railway(PostgreSQL, Suno API)는 그대로 두고, **서비스 하나(오케스트레이터)** 만 추가하면 됨.

### 구현 시 유의사항

- Suno 폴링, Fish/Hedra/Runway 호출, FFmpeg, YouTube 업로드 등은 **오케스트레이터 API 내부**에서 Python/Node로 구현.
- API 키·DB URL 등은 **Railway Variables**로만 관리하고, n8n에는 “호출용 URL + 필요 시 API 키 1개”만 두면 됨.

---

## 4. B. 풀 Python/Node 파이프라인 (n8n 제거)

### 아이디어

- n8n을 아예 제거.
- **하나의 스크립트**(예: `scripts/daily_pipeline.py`)가:
  - DB 연결 → pending 스토리 조회 → Claude → Suno/Fish/Hedra/Runway → FFmpeg → YouTube → DB 업데이트  
  를 순서대로 수행.

### 실행 방법 (택 1)

1. **Railway Cron Job**  
   - Railway에서 “Cron Job” 서비스를 두고, 매일 지정 시각에 `python scripts/daily_pipeline.py` 실행.  
   - 또는 기존 서비스 하나에 **Cron 트리거**를 두고 같은 스크립트 실행.

2. **GitHub Actions**  
   - `.github/workflows/daily.yml`에서 `schedule: cron('0 3 * * *')` 로 매일 03:00에  
     - Railway/다른 호스트의 “파이프라인 API”를 호출하거나  
     - self-hosted runner에서 `python scripts/daily_pipeline.py` 실행.

3. **로컬/서버 cron**  
   - 한 대 서버나 본인 PC에서 `crontab`으로 매일 같은 시각에 스크립트 실행.

### 장점

- n8n 설정·Credential·워크플로우 임포트 문제가 **완전히 사라짐**.
- 전체 흐름이 **한 코드베이스**에 있어서 읽기·수정·디버깅이 가장 단순함.

### 단점

- 스크립트가 길어지면 “오케스트레이터 API”처럼 모듈을 나누는 게 좋음.  
  → 결국 A와 비슷한 코드 구조가 되고, “API로 감쌀지, 스크립트로만 둘지”만 선택하면 됨.

---

## 5. C. GitHub Actions 스케줄

### 아이디어

- 자동화 “트리거”만 GitHub Actions에 두는 방법.
- **옵션 1**: 매일 cron으로 **Railway에 배포한 오케스트레이터 API**를 `curl`/`fetch`로 호출.  
  → 실제 일은 Railway 쪽에서 수행.
- **옵션 2**: Actions에서 **Python 스크립트**를 실행 (DB/API 키는 Secrets에 저장).  
  → 실행 시간 제한(무료 6분 등)과 보안(Secrets 노출 최소화)만 잘 설계.

### 장점

- 워크플로우 정의가 **YAML로 버전 관리**됨.
- n8n을 트리거 용도로만 쓰던 부분을 완전히 대체 가능.

### 단점

- 무료: 공개 repo 2000분/월, 비공개 2000분/월 제한.
- 장시간(수십 분) 파이프라인은 타임아웃이나 비용을 고려해야 함.  
  → 그런 경우에는 “트리거만 Actions, 실제 실행은 Railway 오케스트레이터”가 안전.

---

## 6. D. Inngest / Trigger.dev

- **Inngest**: 이벤트/스케줄 기반으로 함수 실행. 재시도·병렬 처리 지원.
- **Trigger.dev**: 백그라운드 잡 큐 + 스케줄.

둘 다 “코드로 워크플로우 정의”가 가능해서, n8n의 **시각적 노드 대신 코드**로 같은 흐름을 구현할 수 있음.  
무료 티어가 있어서 “n8n 대체”로 검토할 만함. 다만 새 서비스 도입과 개념 학습이 필요함.

---

## 7. E. n8n만 단순화 (노드 수 축소)

- n8n은 유지하되, **“Cron → HTTP Request 1회”** 만 두고,
- 위에서 말한 **오케스트레이터 API**가 나머지 전부 처리하게 하면,
- n8n Credential은 **PostgreSQL, Anthropic, Hedra, Runway, Fish, YouTube** 등을 **전부 제거**해도 됨.  
  (오케스트레이터가 DB/외부 API 직접 호출하므로.)

---

## 8. 정리 및 추천 순서

1. **가장 추천 (빠르게 단순화)**  
   - **A. 오케스트레이터 API + 단순 트리거**  
   - 기존 Railway·DB·Suno API는 유지하고, **오케스트레이터 서비스 1개** 추가.  
   - n8n은 **Cron + HTTP 1번**으로 축소하거나, 트리거만 **GitHub Actions**로 옮겨도 됨.

2. **n8n을 완전히 빼고 싶다면**  
   - **B. 풀 Python 파이프라인**  
   - `daily_pipeline.py` (또는 모듈화된 오케스트레이터) + Railway Cron 또는 GitHub Actions.

3. **트리거만 코드로 두고 싶다면**  
   - **C. GitHub Actions**로 매일 “오케스트레이터 API 호출” 한 번.

4. **n8n은 두되, Credential·노드 수를 줄이고 싶다면**  
   - **E**: 로직을 오케스트레이터로 옮기고, n8n은 Cron + HTTP 1번.

원하시면 **A안** 기준으로  
- `video-processor-api` 또는 새 서비스 이름  
- 엔드포인트 예: `POST /run-daily`  
- 내부 단계(DB 조회 → Claude → … → YouTube)를 함수/모듈로 나누는 예시 구조  
까지 구체적인 설계안이나 코드 스켈레톤을 이어서 작성해 드리겠습니다.
