# ✅ 실행 전 체크리스트 & 구조 개선점

## 🎯 실행 흐름 확인

### ✅ 현재 구조 (정상 작동)

```
1. Cron Trigger (AM 3:00 매일)
   ↓
2. PostgreSQL: 구절 3개 조회 (순차)
   - SELECT ... JOIN book_order
   - ORDER BY book_number, chapter, verse
   - LIMIT 3
   ↓
3. Claude → Fish Audio → Hedra → Runway → Suno (병렬)
   ↓
4. FFmpeg 합성 → 썸네일 생성 → YouTube 업로드
   ↓
5. PostgreSQL: 최종 업데이트
   - status = 'completed' ✅
```

**결론**: ✅ **실행하면 창세기 1:1부터 순서대로 올라갑니다!**

---

## 🔴 Critical: 실행 전 필수 작업

### 1. ⚠️ 성경 데이터 입력 (필수!)

**현재 상태**: ❌ 성경 데이터 없음 (샘플 20개만)

**해결 방법**:
```bash
# Step 1: 책 순서 테이블 생성
export DATABASE_URL="postgresql://user:pass@railway.app:5432/railway"
psql $DATABASE_URL < database/book_order.sql

# Step 2: 성경 데이터 수집 (31,102개 구절)
pip install psycopg2-binary requests
python3 scripts/fetch_bible_data.py

# Step 3: 캐릭터 자동 할당
python3 scripts/assign_characters.py

# 확인:
psql $DATABASE_URL -c "SELECT COUNT(*) FROM scripture WHERE status='pending';"
# 예상 결과: 31102 (또는 비슷한 수)
```

---

### 2. ⚠️ n8n Credentials 설정 (필수!)

**Railway n8n에서 설정**:
```
1. PostgreSQL Credentials
   - Name: Railway PostgreSQL
   - Host: containers-us-west-XXX.railway.app
   - Port: XXXX
   - Database: railway
   - User: postgres
   - Password: ****

2. Claude API (Anthropic)
   - API Key: sk-ant-****

3. Fish Audio API
   - API Key: ****

4. Hedra API
   - API Key: ****

5. Runway API
   - API Key: ****

6. YouTube OAuth2
   - Client ID: ****
   - Client Secret: ****
   - Refresh Token: ****
```

---

### 3. ⚠️ FFmpeg & Python 스크립트 배포

**Railway에 스크립트 업로드**:
```bash
# scripts/ffmpeg_compose_3phase.sh
# scripts/generate_thumbnail.py

# 실행 권한 부여
chmod +x scripts/ffmpeg_compose_3phase.sh
```

---

## 🟡 High: 구조적 개선점

### 1. 에러 처리 로직 추가 (30분)

**문제**: 현재 API 실패 시 전체 워크플로우 중단

**해결 방법**:
```json
// 모든 API 노드에 추가
{
  "continueOnFail": true,
  "retryOnFail": true,
  "maxTries": 3,
  "waitBetweenTries": 5000
}
```

**실패 시 status 업데이트**:
```json
{
  "id": "error-handler",
  "name": "PostgreSQL: 에러 기록",
  "parameters": {
    "operation": "executeQuery",
    "query": "UPDATE scripture SET status = 'failed', processing_error = $1 WHERE id = $2",
    "additionalFields": {
      "queryParameters": "={{ [$json.error.message, $json.scripture_id] }}"
    }
  }
}
```

---

### 2. 수동 실행 방법 (테스트용)

**Cron 기다리지 않고 즉시 실행**:

**Option 1: n8n UI**
```
1. Railway n8n 접속
2. complete_pipeline 워크플로우 열기
3. "Execute Workflow" 버튼 클릭
4. 즉시 실행 (Cron 무시)
```

**Option 2: Manual Trigger 노드 추가**
```json
{
  "id": "manual-trigger",
  "name": "Manual Trigger (테스트용)",
  "type": "n8n-nodes-base.manualTrigger",
  "position": [250, 400]
}
```

---

### 3. Cron 빈도 조정 (선택)

**현재**: AM 3:00 (하루 3개)  
**예상**: 31,102개 ÷ 3 = **10,367일 (28.4년)**

**개선 옵션**:

#### Option A: 하루 2회
```json
{
  "cronExpression": "0 3,15 * * *"  // AM 3:00, PM 3:00
}
// 결과: 하루 6개 → 14.2년
```

#### Option B: 하루 3회
```json
{
  "cronExpression": "0 3,11,19 * * *"  // AM 3:00, 11:00, PM 7:00
}
// 결과: 하루 9개 → 9.5년
```

#### Option C: 매 8시간
```json
{
  "cronExpression": "0 */8 * * *"  // 매 8시간마다
}
// 결과: 하루 9개 → 9.5년
```

#### Option D: LIMIT 증가 (권장)
```sql
-- complete_pipeline.json 쿼리 수정
... LIMIT 10  -- 3 → 10으로 변경
```
```json
{
  "cronExpression": "0 3 * * *"  // AM 3:00
}
// 결과: 하루 10개 → 8.5년
```

---

### 4. 모니터링 & 알림 추가 (1시간)

**Telegram 알림 노드 추가**:
```json
{
  "id": "telegram-notification",
  "name": "Telegram: 일일 리포트",
  "type": "n8n-nodes-base.telegram",
  "parameters": {
    "chatId": "YOUR_CHAT_ID",
    "text": "✅ 오늘 생성된 영상:\n- {{ $json.book_name }} {{ $json.chapter }}:{{ $json.verse }}\n- YouTube: {{ $json.youtube_url }}\n- 상태: {{ $json.status }}"
  }
}
```

**위치**: PostgreSQL 최종 업데이트 이후

---

### 5. Dry-run 테스트 모드 (1시간)

**테스트용 플래그 추가**:
```json
{
  "id": "set-test-mode",
  "name": "Set: 테스트 모드",
  "type": "n8n-nodes-base.set",
  "parameters": {
    "values": {
      "boolean": [
        {
          "name": "isDryRun",
          "value": true  // false로 변경 시 실제 실행
        }
      ]
    }
  }
}
```

**테스트 모드 시**:
- YouTube 업로드 건너뛰기
- DB status 업데이트 안 함
- 로그만 출력

---

## 🟢 Medium: 추가 개선 (Phase 2)

### 1. DB 트랜잭션 처리
```sql
-- 시작 시 status = 'processing'
BEGIN;
UPDATE scripture SET status = 'processing' WHERE id = $1;

-- 성공 시 status = 'completed'
-- 실패 시 ROLLBACK
```

### 2. 재시도 큐 시스템
```sql
-- 실패한 구절 자동 재시도
SELECT * FROM scripture 
WHERE status = 'failed' 
  AND created_at > NOW() - INTERVAL '7 days'
ORDER BY created_at DESC
LIMIT 3;
```

### 3. API 비용 추적
```sql
ALTER TABLE scripture 
ADD COLUMN api_cost_usd REAL DEFAULT 0.0;

-- 예상 비용 계산
UPDATE scripture 
SET api_cost_usd = 
  (0.10 + -- Claude
   0.05 + -- Fish Audio
   0.30 + -- Hedra
   0.50 + -- Runway
   0.20)  -- Suno
WHERE status = 'completed';
```

---

## 📊 실행 전 최종 체크리스트

### 🔴 필수 (Critical)
```
□ 성경 데이터 입력 (31,102개 구절)
  - book_order.sql 실행
  - fetch_bible_data.py 실행
  - assign_characters.py 실행

□ n8n Credentials 설정
  - PostgreSQL
  - Claude API
  - Fish Audio API
  - Hedra API
  - Runway API
  - YouTube OAuth2

□ FFmpeg 스크립트 배포
  - ffmpeg_compose_3phase.sh
  - generate_thumbnail.py

□ 테스트 실행 (1개 구절)
  - Manual Trigger로 테스트
  - 전체 파이프라인 동작 확인
  - YouTube 업로드 성공 확인
```

### 🟡 권장 (High)
```
□ 에러 처리 로직 추가
  - continueOnFail: true
  - retryOnFail: true
  - 실패 시 status = 'failed'

□ Cron 빈도 조정
  - LIMIT 3 → 10 (권장)
  - 또는 하루 2-3회 실행

□ 모니터링 추가
  - Telegram 알림
  - 일일 리포트
```

### 🟢 선택 (Medium)
```
□ Dry-run 테스트 모드
□ DB 트랜잭션 처리
□ API 비용 추적
□ 재시도 큐 시스템
```

---

## 🚀 실행 순서 (처음 실행 시)

### 1단계: 데이터 준비
```bash
# 1. 책 순서 테이블
psql $DATABASE_URL < database/book_order.sql

# 2. 성경 데이터 수집
python3 scripts/fetch_bible_data.py

# 3. 캐릭터 할당
python3 scripts/assign_characters.py

# 4. 확인
psql $DATABASE_URL -c "
SELECT 
  b.book_number,
  s.book_name, 
  s.chapter, 
  s.verse,
  LEFT(s.korean_text, 30) as preview
FROM scripture s
JOIN book_order b ON s.book_name = b.book_name_korean
WHERE s.status = 'pending'
ORDER BY b.book_number, s.chapter, s.verse
LIMIT 5;
"
# 예상 결과:
# 1 | 창세기 | 1 | 1 | 태초에 하나님이 천지를 창조하시니라...
# 1 | 창세기 | 1 | 2 | 땅이 혼돈하고 공허하며...
# 1 | 창세기 | 1 | 3 | 하나님이 이르시되 빛이 있으라...
```

### 2단계: n8n 설정
```
1. Railway n8n 접속
2. Credentials 설정 (PostgreSQL, APIs)
3. complete_pipeline.json 임포트
4. 노드 연결 확인
```

### 3단계: 테스트 실행
```
1. "Execute Workflow" 클릭 (수동 실행)
2. 실행 로그 확인
3. DB에서 상태 확인:
   SELECT * FROM scripture WHERE status='completed' LIMIT 1;
4. YouTube 업로드 확인
```

### 4단계: Cron 활성화
```
1. Cron Trigger 활성화
2. 다음날 AM 3:00 자동 실행 대기
3. 매일 창세기부터 순차적으로 3개씩 생성
```

---

## 🎯 예상 결과

### 첫 실행 (테스트)
```
✅ 창세기 1:1 → YouTube 업로드
✅ DB status = 'completed'
✅ 다음 실행 시 창세기 1:2부터 시작
```

### 일주일 후
```
✅ 21개 영상 생성 (하루 3개 × 7일)
✅ 창세기 1:1 ~ 1:21
✅ YouTube 채널에 21개 숏츠
```

### 1년 후
```
✅ 1,095개 영상 생성 (하루 3개 × 365일)
✅ 창세기 1:1 ~ 창세기 약 44장
✅ 성경 전체의 약 3.5% 완성
```

### 완전 완성
```
⏳ 약 28.4년 (하루 3개 기준)
⏳ 약 8.5년 (하루 10개 기준, LIMIT 10)
⏳ 약 2.8년 (하루 30개 기준, 하루 3회 × 10개)
```

---

## 💡 권장 설정 (최종)

### 현실적 목표: **5년 내 완성**

**설정**:
```json
{
  "cronExpression": "0 3,15 * * *",  // 하루 2회
  "query": "... LIMIT 8"  // 한 번에 8개
}
```

**결과**:
- 하루 16개 영상
- 31,102 ÷ 16 = **1,944일** (**5.3년**)
- API 비용: 약 $16/일 (하루 16개)
- 월 비용: 약 $480

---

## 🎉 결론

**Q**: "이제 구조상 개선점 뭐있어? 실행만하면 1장1절부터 올라가게되는건가?"

**A**:
```
✅ 구조는 거의 완벽!
✅ 실행하면 창세기 1:1부터 순차적으로 올라감!

🔴 실행 전 필수:
  1. 성경 데이터 입력 (fetch_bible_data.py)
  2. n8n Credentials 설정
  3. 테스트 실행 1회

🟡 구조 개선 권장:
  1. 에러 처리 로직
  2. Cron 빈도/LIMIT 조정 (28년 → 5년)
  3. 모니터링 & 알림

실행만 하면 창세기 1:1부터 자동으로 올라갑니다! 🚀
```
