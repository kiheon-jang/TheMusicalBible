# 🚀 The Musical Bible - 설정 및 배포 통합 가이드

**최종 업데이트**: 2026년 1월 25일

---

## 📋 목차

1. [빠른 시작 (5분)](#빠른-시작)
2. [Credentials 설정](#credentials-설정)
3. [데이터베이스 초기화](#데이터베이스-초기화)
4. [Suno API 설정](#suno-api-설정)
5. [n8n 워크플로우 임포트](#n8n-워크플로우-임포트)
6. [YouTube API 설정](#youtube-api-설정)
7. [트러블슈팅](#트러블슈팅)

---

## 🎯 빠른 시작

### 필수 준비물
- Railway 계정 (PostgreSQL + n8n + Suno API 배포 완료)
- Suno Pro 구독 ($10/월)
- API 키들 (Claude, Hedra, Fish Audio, Runway)
- YouTube 채널

### 5분 설정 순서
```
1. Suno 쿠키 → Railway 환경변수 설정
2. n8n Credentials 설정 (6개)
3. 워크플로우 임포트
4. 테스트 실행
```

---

## 🔐 Credentials 설정

### n8n 접속 정보
```
URL: https://n8n-production-1d6b.up.railway.app
Email: xaqwer@gmail.com
Password: Wkdrlgjs2@
```

### 1. Claude API (1분)
```
Credential Type: Header Auth
Name: x-api-key
Value: [API_KEYS.txt 참고]
```

### 2. Hedra API (1분)
```
Credential Type: Header Auth
Name: X-API-Key
Value: [API_KEYS.txt 참고]
```

### 3. Fish Audio API (1분)
```
Credential Type: Header Auth
Name: Authorization
Value: [API_KEYS.txt 참고]
```

### 4. Runway API (1분)
```
Credential Type: Header Auth
Name: Authorization
Value: Bearer [API_KEYS.txt 참고]
⚠️ "Bearer " 포함!
```

### 5. YouTube API (2분)
```
Credential Type: Google OAuth2 API
Client ID: [YOUTUBE_CREDENTIALS.txt 참고]
Client Secret: [YOUTUBE_CREDENTIALS.txt 참고]

Scope:
https://www.googleapis.com/auth/youtube.upload
https://www.googleapis.com/auth/youtube

→ "Connect my account" 클릭
→ Google 계정 승인
```

### 6. PostgreSQL (1분)
```
Credential Type: Postgres
Host: maglev.proxy.rlwy.net
Port: 15087
Database: railway
User: postgres
Password: [Railway Dashboard에서 확인]

→ Test Connection 클릭
```

---

## 🗄️ 데이터베이스 초기화

### 자동 초기화 (권장)
```bash
cd /Users/giheonjang/Documents/project/TMB
source venv/bin/activate
python scripts/init_postgres_direct.py
```

### 수동 초기화
```sql
-- Railway PostgreSQL 접속 후:
\i database/init_postgresql.sql
\i database/seed_data.sql
```

### 확인
```sql
SELECT COUNT(*) FROM scripture;        -- 성경 구절
SELECT COUNT(*) FROM character_voices; -- 캐릭터 (10개)
```

---

## 🎵 Suno API 설정

### 1. Suno 쿠키 가져오기 (2분)

#### 방법
```
1. https://suno.com/ 접속 → 로그인
   (Pro 구독 필요: $10/월)

2. F12 (개발자 도구)

3. Application 탭 → Cookies → https://suno.com

4. 전체 Cookie 문자열 복사
```

#### Cookie 형식
```
__client=abc123...;
__session=def456...;
__stripe_mid=ghi789...;
__stripe_sid=jkl012...
```

### 2. Railway에 쿠키 설정 (1분)

```bash
# Railway CLI 사용
railway variables set SUNO_COOKIE="복사한_쿠키_전체"

# 또는 Railway Dashboard
# → suno-api 서비스 → Variables → SUNO_COOKIE 추가
```

### 3. Suno API 테스트

```bash
curl https://suno-api-production-ac35.up.railway.app/get_credits
```

**응답 예시**:
```json
{
  "credits_left": 500,
  "period": "monthly",
  "monthly_limit": 2500
}
```

---

## 📥 n8n 워크플로우 임포트

### 1. n8n 접속
```
https://n8n-production-1d6b.up.railway.app
```

### 2. 워크플로우 임포트 순서

#### 필수 워크플로우 (3개)
```
1. workflows/morning_batch.json
   → AM 2:00 프롬프트 생성

2. workflows/evening_generation.json
   → PM 2:00 영상 생성 및 업로드

3. workflows/daily_monitoring.json
   → AM 10:00 YouTube 통계 수집
```

#### 선택 워크플로우 (3개)
```
4. workflows/suno_cookie_monitor.json
   → 매시간 Suno 쿠키 상태 확인

5. workflows/suno_with_polling.json
   → Suno 음악 생성 (Polling)

6. workflows/music_api_fallback.json
   → 음악 API Fallback 시스템
```

### 3. 임포트 방법
```
1. Workflows 메뉴 클릭
2. "Import from File" 클릭
3. JSON 파일 선택
4. "Import" 클릭
5. Credentials 연결 확인
6. "Save" 클릭
```

### 4. Cron 트리거 활성화
```
각 워크플로우에서:
→ Cron Trigger 노드 클릭
→ "Execute Workflow" 활성화
```

---

## 📺 YouTube API 설정

### 1. Google Cloud Console 설정

#### Step 1: 프로젝트 생성
```
1. https://console.cloud.google.com 접속
2. 새 프로젝트 생성: "The Musical Bible"
```

#### Step 2: YouTube Data API v3 활성화
```
1. API 및 서비스 → 라이브러리
2. "YouTube Data API v3" 검색
3. 사용 설정 클릭
```

#### Step 3: OAuth 2.0 클라이언트 ID 생성
```
1. API 및 서비스 → 사용자 인증 정보
2. "사용자 인증 정보 만들기" → OAuth 클라이언트 ID
3. 애플리케이션 유형: 웹 애플리케이션
4. 승인된 리디렉션 URI:
   https://n8n-production-1d6b.up.railway.app/rest/oauth2-credential/callback
5. 생성 후 Client ID / Client Secret 복사
```

### 2. n8n에서 YouTube Credential 설정

```
1. n8n → Credentials → Add Credential
2. "Google OAuth2 API" 선택
3. Client ID / Client Secret 입력
4. Scope 추가:
   - https://www.googleapis.com/auth/youtube.upload
   - https://www.googleapis.com/auth/youtube
5. "Connect my account" 클릭
6. Google 계정 승인
7. 초록색 체크 표시 확인
```

---

## 🔧 트러블슈팅

### Suno API 오류

#### 문제: "Unauthorized" 또는 "Invalid cookie"
```bash
# 해결: 쿠키 재설정
1. Suno.com에서 쿠키 다시 복사
2. Railway variables set SUNO_COOKIE="새_쿠키"
3. Suno API 재시작
```

#### 문제: "Credit balance too low"
```
해결: Suno Pro 구독 확인 및 크레딧 충전
```

### Claude API 오류

#### 문제: "Credit balance too low"
```
해결: https://console.anthropic.com/settings/billing
최소 $5 충전 권장
```

### PostgreSQL 연결 오류

#### 문제: "Connection refused"
```bash
# 확인:
railway status

# 재시작:
railway restart
```

### n8n 워크플로우 실행 오류

#### 문제: "Credential not found"
```
해결:
1. Credentials 메뉴에서 모든 Credential 확인
2. 각 워크플로우 노드에서 Credential 재연결
3. Test Connection 실행
```

#### 문제: "SQLite node not found"
```
해결: SQLite → PostgreSQL 노드로 변경 필요
CODE_FIXES_PRIORITY.md 참고
```

### YouTube 업로드 오류

#### 문제: "Quota exceeded"
```
해결: YouTube API 할당량 확인
기본 할당량: 일 10,000 units
업로드 1회 = 1,600 units (일 6회 가능)
```

#### 문제: "Invalid credentials"
```
해결:
1. YouTube Credential 재승인
2. OAuth 토큰 갱신
3. Redirect URI 확인
```

---

## ✅ 설정 완료 체크리스트

### Railway 인프라
- [ ] PostgreSQL 배포 및 초기화
- [ ] n8n 배포 및 접속 확인
- [ ] Suno API 배포 및 작동 확인

### n8n Credentials
- [ ] Claude API
- [ ] Hedra API
- [ ] Fish Audio API
- [ ] Runway API
- [ ] YouTube API (OAuth 연결)
- [ ] PostgreSQL

### 워크플로우
- [ ] Morning Batch 임포트 및 활성화
- [ ] Evening Generation 임포트 및 활성화
- [ ] Daily Monitoring 임포트 및 활성화
- [ ] Suno Cookie Monitor (선택)
- [ ] Suno Polling (선택)
- [ ] Music API Fallback (선택)

### 테스트
- [ ] Suno API 크레딧 확인
- [ ] Claude API 응답 확인
- [ ] PostgreSQL 쿼리 테스트
- [ ] YouTube 채널 권한 확인
- [ ] 전체 파이프라인 1회 수동 실행

---

## 📞 지원

- **n8n**: https://n8n-production-1d6b.up.railway.app
- **Suno API**: https://suno-api-production-ac35.up.railway.app
- **Email**: xaqwer@gmail.com

---

## 📚 관련 문서

- **코드 리뷰**: `CODE_REVIEW_REPORT.md`
- **수정 가이드**: `CODE_FIXES_PRIORITY.md`
- **API 검증**: `API_ENDPOINTS_VERIFICATION.md`
- **프로젝트 개요**: `README.md`
- **빠른 시작**: `QUICK_START.md`

---

**🎉 모든 설정이 완료되었습니다!**

이제 Cron 트리거를 활성화하고 자동화를 시작하세요! 🚀
