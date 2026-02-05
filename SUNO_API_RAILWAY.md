---
date: 2026-02-01
project: 10_Projects/project
tags: ['project']
---
# Railway Suno API 설정 가이드 (SunoAI-API)

**변경됨**: gcui-art/suno-api → **[SunoAI-API/Suno-API](https://github.com/SunoAI-API/Suno-API)**

2Captcha 유료 서비스가 필요 없는 직접 API 호출 방식으로 변경되었습니다.

## 1. 새 API의 장점

| 항목 | gcui-art (이전) | SunoAI-API (현재) |
|------|-----------------|-------------------|
| 2Captcha | ✅ 필수 (유료) | ❌ 불필요 |
| 방식 | Playwright 브라우저 자동화 | 직접 API 호출 |
| 환경 변수 | SUNO_COOKIE, TWOCAPTCHA_KEY, BROWSER 등 | SESSION_ID, COOKIE만 |

## 2. Railway 배포 방법

### Step 1: 기존 서비스 삭제
1. Railway 대시보드 접속
2. 기존 suno-api 서비스 삭제 또는 중지

### Step 2: 새 서비스 생성
1. Railway 대시보드 → **New Project** → **Deploy from GitHub repo**
2. Repository URL: `https://github.com/SunoAI-API/Suno-API`
3. Deploy 클릭

### Step 3: 환경 변수 설정
Railway Variables에 다음 두 가지만 설정:

| 변수 | 설명 | 값 얻는 방법 |
|------|------|-------------|
| `SESSION_ID` | Suno 세션 ID | 아래 "쿠키 추출 방법" 참고 |
| `COOKIE` | Suno 쿠키 전체 | 아래 "쿠키 추출 방법" 참고 |

### Step 4: 배포 URL 확인
배포 완료 후 Railway에서 생성된 URL 확인 (예: `https://suno-api-xxx.up.railway.app`)

## 3. 쿠키 추출 방법

1. [suno.com/create](https://suno.com/create) 접속 및 로그인
2. 브라우저 개발자 도구 열기 (`F12`)
3. **Network** 탭 선택
4. 페이지 새로고침
5. `?__clerk_api_version` 포함된 요청 찾기
6. 해당 요청 클릭 → **Headers** 탭

### SESSION_ID 찾기
- URL에서 `sessions/` 뒤의 값
- 예: `https://clerk.suno.com/v1/client/sessions/sess_xxxxx/tokens`
- → `SESSION_ID` = `sess_xxxxx`

### COOKIE 찾기
- Headers → **Cookie** 값 전체 복사

## 4. API 엔드포인트

| 기능 | 엔드포인트 | 메서드 |
|------|-----------|--------|
| 음악 생성 (Custom Mode) | `/generate` | POST |
| 음악 생성 (Description Mode) | `/generate/description-mode` | POST |
| 상태 확인 | `/feed/{audio_id}` | GET |
| 크레딧 확인 | `/get_credits` | GET |
| 가사 생성 | `/generate/lyrics/` | POST |

### Custom Mode 요청 형식 (워크플로우 사용)

```json
{
  "prompt": "가사 내용",
  "mv": "chirp-v3-5",
  "title": "곡 제목",
  "tags": "cinematic orchestral epic",
  "negative_tags": ""
}
```

### Description Mode 요청 형식

```json
{
  "gpt_description_prompt": "설명 프롬프트",
  "make_instrumental": false,
  "mv": "chirp-v3-5"
}
```

## 5. 테스트 방법

### 크레딧 확인
```bash
curl https://YOUR_RAILWAY_URL/get_credits
```

정상 응답 예:
```json
{
  "credits_left": 2500,
  "period": "month",
  "monthly_limit": 2500,
  "monthly_usage": 0
}
```

### 음악 생성 테스트
```bash
curl -X POST https://YOUR_RAILWAY_URL/generate \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Test lyrics here",
    "mv": "chirp-v3-5",
    "title": "Test Song",
    "tags": "pop upbeat",
    "negative_tags": ""
  }'
```

## 6. n8n 워크플로우 URL 변경

Railway 배포 완료 후, n8n 워크플로우의 URL을 새 Railway URL로 변경해야 합니다.

현재 워크플로우에 설정된 URL:
- `https://suno-api-production-ac35.up.railway.app/generate`
- `https://suno-api-production-ac35.up.railway.app/feed/{id}`

→ 새 Railway URL로 교체 필요

## 7. 문제 해결

### "Failed to get session id" 오류
- SESSION_ID가 잘못되었거나 만료됨
- Suno에 다시 로그인 후 새 SESSION_ID 추출

### "Invalid token" 오류
- COOKIE가 만료됨
- Suno에 다시 로그인 후 새 COOKIE 추출

### 토큰 자동 갱신
- SunoAI-API는 5초마다 자동으로 토큰을 갱신함
- 장시간 (수일) 미사용 시 재로그인 필요할 수 있음

## 8. 참고 링크

- [SunoAI-API/Suno-API GitHub](https://github.com/SunoAI-API/Suno-API)
- [Suno.ai](https://suno.ai)
