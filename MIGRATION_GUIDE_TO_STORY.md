# 🔄 스토리 단위 전환 가이드

## 🎯 변경 사항 요약

### Before (구절 단위) ❌
```
- 31,102개 구절
- 각 구절 = 1개 영상 (30초)
- 비용: $70,290
- 완성: 8.5년
```

### After (스토리 단위) ✅
```
- 3,500개 스토리
- 설교 단위 = 1개 영상 (60-180초)
- 비용: $7,910 (89% 절감!)
- 완성: 1년 이내
```

---

## 📋 전환 단계

### Step 1: DB 스키마 추가 (5분)

```bash
export DATABASE_URL="postgresql://user:pass@railway.app/railway"

# 스토리 단위 테이블 생성
psql $DATABASE_URL < database/story_units_schema.sql

# 확인
psql $DATABASE_URL -c "SELECT * FROM story_units LIMIT 1;"
```

**생성되는 테이블**:
- `story_units`: 스토리 단위 메인 테이블
- `verse_to_story`: 구절 ↔ 스토리 매핑

---

### Step 2: 스토리 단위 분석 (2-3시간)

```bash
# Claude API 키 설정
export CLAUDE_API_KEY="sk-ant-..."
export DATABASE_URL="postgresql://..."

# 필요한 패키지 설치
pip install anthropic psycopg2-binary

# 테스트: 창세기 1-5장
python3 scripts/analyze_story_units.py --test

# 결과 확인
psql $DATABASE_URL -c "SELECT id, book_name, verses_range, title, verse_count FROM story_units LIMIT 10;"
```

**예상 결과**:
```
id | book_name | verses_range | title          | verse_count
---+-----------+--------------+----------------+-------------
1  | 창세기    | 1:1-2:3      | 천지 창조      | 34
2  | 창세기    | 2:4-25       | 에덴동산       | 22
3  | 창세기    | 3:1-24       | 선악과 사건    | 24
```

---

### Step 3: 전체 성경 분석 (2-3시간, 선택)

```bash
# 창세기 전체 분석 (50장 → 약 100개 스토리)
python3 scripts/analyze_story_units.py --genesis

# 또는 전체 성경 분석 (66권 → 약 3,500개 스토리)
# 주의: Claude API 비용 발생 ($20-30 예상)
python3 scripts/analyze_story_units.py --all
```

**비용 계산**:
```
창세기 분석: 약 100개 스토리 × $0.02 = $2
전체 분석: 약 3,500개 스토리 × $0.02 = $70
```

---

### Step 4: 워크플로우 교체 (10분)

#### Option A: 기존 워크플로우 교체 (권장)

```bash
# Railway n8n 접속
# 1. 기존 complete_pipeline 비활성화
# 2. complete_pipeline_story.json 임포트
# 3. Credentials 연결 (같은 것 사용)
# 4. 활성화
```

#### Option B: 둘 다 유지 (테스트용)

```
complete_pipeline.json (구절 단위)
  → 비활성화, 백업용

complete_pipeline_story.json (스토리 단위)
  → 활성화, 메인
```

---

### Step 5: 테스트 실행 (5분)

```bash
# Railway n8n에서
1. complete_pipeline_story 워크플로우 열기
2. "Execute Workflow" 클릭
3. 실행 로그 확인
4. DB 확인:
   psql $DATABASE_URL -c "SELECT * FROM story_units WHERE status='completed';"
```

---

## 🔧 주요 변경 사항

### 1. DB 쿼리 변경

**Before**:
```sql
SELECT s.id, s.book_name, s.chapter, s.verse, s.korean_text, ...
FROM scripture s
WHERE s.status = 'pending'
ORDER BY b.book_number, s.chapter, s.verse
LIMIT 3
```

**After**:
```sql
SELECT s.id, s.book_name, s.verses_range, s.title, s.verse_count, ...
FROM story_units s
WHERE s.status = 'pending'
ORDER BY b.book_number, s.id
LIMIT 3
```

---

### 2. Claude 프롬프트 변경

**Before (30초, 1개 구절)**:
```
"성경 구절: 태초에 하나님이 천지를 창조하시니라
30초 영상을 위한 프롬프트 생성"
```

**After (60-180초, 여러 구절)**:
```
"스토리: 천지 창조 (창세기 1:1-2:3, 34개 구절)
핵심 주제: 하나님의 질서 있는 7일 창조
90초 영상을 위한 완전한 서사 프롬프트 생성"
```

---

### 3. 영상 길이 조정

**Before**:
```javascript
phase1_duration: 8,
phase2_duration: 10,
phase3_duration: 12,
// 총 30초
```

**After**:
```javascript
phase1_duration: Math.ceil(story_duration * 0.25),  // 25%
phase2_duration: Math.ceil(story_duration * 0.35),  // 35%
phase3_duration: Math.ceil(story_duration * 0.40),  // 40%
// 총 60-180초 (스토리 길이에 따라)
```

---

## 📊 비교표

| 항목 | 구절 단위 | 스토리 단위 | 개선 |
|------|-----------|-------------|------|
| **영상 개수** | 31,102개 | 3,500개 | 89% ↓ |
| **평균 길이** | 30초 | 90초 | 3배 ↑ |
| **구절당 비용** | $2.26 | - | - |
| **스토리당 비용** | - | $2.26 | 동일 |
| **총 비용** | $70,290 | $7,910 | 89% ↓ |
| **완성 기간** | 8.5년 | 1년 | 88% ↓ |
| **콘텐츠 품질** | ⭐⭐ | ⭐⭐⭐⭐⭐ | 향상 |

---

## ✅ 체크리스트

### 필수 작업
```
□ story_units_schema.sql 실행
□ analyze_story_units.py --test 실행
□ 테스트 스토리 3-5개 생성 확인
□ complete_pipeline_story.json 임포트
□ Credentials 연결
□ 테스트 실행 1회
```

### 권장 작업
```
□ 창세기 전체 분석 (--genesis)
□ 기존 워크플로우 백업
□ DB 백업 (스냅샷)
□ 비용 모니터링 설정
```

### 선택 작업
```
□ 전체 성경 분석 (--all)
□ 기존 구절 데이터 유지/삭제 결정
□ 스토리 품질 검증 (신학 자문)
```

---

## 🚨 주의사항

### 1. 기존 데이터 처리

**옵션 A: 병행 운영**
```sql
-- scripture 테이블: 그대로 유지
-- story_units 테이블: 새로 추가
-- 둘 다 사용 가능
```

**옵션 B: 완전 전환**
```sql
-- scripture 테이블: 백업 후 비활성화
-- story_units 테이블: 메인으로 사용
```

### 2. Claude API 비용

```
테스트 (창세기 1-5장): $0.50
창세기 전체: $2
전체 성경: $70

권장: 테스트 → 창세기 → 구약 일부 → 전체
```

### 3. 영상 길이

```
스토리 길이 분포:
- 짧은 스토리: 60초 (20%)
- 중간 스토리: 90초 (60%)
- 긴 스토리: 120-180초 (20%)

FFmpeg 스크립트 수정 필요!
```

---

## 🔄 롤백 방법

만약 문제가 생기면:

```bash
# 1. 기존 워크플로우 재활성화
# complete_pipeline.json 활성화

# 2. story_units 테이블 삭제 (선택)
psql $DATABASE_URL -c "DROP TABLE verse_to_story;"
psql $DATABASE_URL -c "DROP TABLE story_units;"

# 3. 모든 것이 원상태로 복구
```

---

## 📞 문제 해결

### Q: 스토리 분석이 실패합니다
```bash
# Claude API 키 확인
echo $CLAUDE_API_KEY

# DB 연결 확인
psql $DATABASE_URL -c "SELECT 1;"

# 에러 로그 확인
python3 scripts/analyze_story_units.py --test 2>&1 | grep ERROR
```

### Q: 스토리가 너무 길거나 짧습니다
```python
# analyze_story_units.py 수정
# 프롬프트에 추가:
"영상 길이: 60-120초 권장 (최소 40초, 최대 180초)"
```

### Q: 신학적으로 이상한 그룹핑
```bash
# 수동 수정
psql $DATABASE_URL

UPDATE story_units 
SET verses_range = '1:1-10',
    verse_count = 10
WHERE id = 1;
```

---

## 🎉 완료 후 확인

```sql
-- 스토리 통계
SELECT 
  COUNT(*) as total_stories,
  AVG(verse_count) as avg_verses,
  AVG(estimated_duration_sec) as avg_duration,
  SUM(verse_count) as total_verses
FROM story_units;

-- 예상 결과:
-- total_stories: 3500
-- avg_verses: 8-10
-- avg_duration: 90
-- total_verses: 31102
```

---

## 💡 다음 단계

1. ✅ 스토리 단위 전환 완료
2. 테스트 영상 10개 제작
3. 품질 검증
4. Cron 활성화
5. 본격 제작 시작!

**이제 1년 내 완성 가능합니다!** 🚀
