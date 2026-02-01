# Railway Suno API 점검 (500 해결)

자체 Suno API는 **Suno 공식 API가 없어** 쿠키/세션으로 Suno 웹과 동일하게 동작하도록 만든 서비스입니다.  
`https://suno-api-production-ac35.up.railway.app/api/generate` 가 500을 반환할 때 아래를 순서대로 확인하세요.

## 1. 토큰 유무 확인

브라우저 또는 curl로 **헬스 체크**를 호출하세요.

```bash
curl -s https://suno-api-production-ac35.up.railway.app/health
```

- **`"token_available": true`** → 토큰 정상. 500이면 Suno 쪽 오류 또는 요청 형식 문제.
- **`"token_available": false`** → Railway 환경 변수 **COOKIE**, **SESSION_ID**가 비어 있거나 만료된 상태입니다.

## 2. Railway 환경 변수 설정

Railway 대시보드 → Suno API 서비스 → **Variables** 탭에서 다음을 설정합니다.

| 변수 | 설명 |
|------|------|
| **COOKIE** | Suno 웹(suno.com) 로그인 후 브라우저 개발자도구 → Application → Cookies 에서 복사한 쿠키 문자열 |
| **SESSION_ID** | Clerk 세션 ID (Suno 로그인 세션과 함께 사용) |
| **BASE_URL** | Suno API 베이스 URL (예: `https://api.suno.com` 등, 사용 중인 값 유지) |

- COOKIE/SESSION_ID는 **Suno 웹에 로그인한 상태**에서 다시 복사해야 합니다.  
- 만료되면 주기적으로 갱신해야 하며, 갱신 후 서비스 **재시작**이 필요할 수 있습니다.

## 3. API 요청 형식 (n8n 워크플로우)

`/api/generate` 는 **CustomModeGenerateParam** 형식을 사용합니다.

| 필드 | 필수 | 설명 |
|------|------|------|
| **prompt** | O | 가사 (한국어 뮤지컬 가사) |
| **mv** | O | 모델 버전 (예: `chirp-v3-0`) |
| **title** | O | 곡 제목 |
| **tags** | O | 스타일/무드 (영문 설명 또는 태그) |
| **negative_tags** | O | 제외할 스타일 (빈 문자열 `""` 가능) |

n8n **Suno: 음악 생성 시작** 노드는 위 필드로 이미 매핑되어 있습니다.  
필드명을 바꾸지 말고, 가사/제목/스타일만 원하는 값으로 넣으면 됩니다.

## 4. 500 시 에러 메시지 확인

수정된 API는 500/503 시 **상세 메시지**를 반환합니다.

- **503** + `"Suno token not available..."`  
  → COOKIE, SESSION_ID 미설정 또는 만료. 2번 항목대로 갱신 후 재시작.
- **500** + `"An error occurred: ..."`  
  → Suno 백엔드 요청 실패. BASE_URL, 쿠키/세션, Suno 서비스 상태 확인.
- **500** + `"<예외 타입>: <메시지>"`  
  → 서버 로그와 함께 메시지 내용으로 원인 추적.

## 5. 코드 변경 요약 (suno-api-fixed)

- **cookie.py**: COOKIE/SESSION_ID가 없어도 서버가 뜨도록 안전 처리.
- **deps.py**: 토큰이 없으면 **503** + 한글 안내 메시지 반환.
- **main.py**: `/generate` 예외 시 **500** + 예외 타입/메시지 반환, **GET /health** 추가.

Railway에 **suno-api-fixed** 변경 사항을 배포한 뒤, `/health` 와 `/api/generate` 를 다시 호출해 보시면 됩니다.
