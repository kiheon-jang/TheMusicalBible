# ⚠️ n8n 워크플로우 수동 임포트 필요

## 상황

n8n API 인증이 실패했습니다 (HTTP 401).  
자동 임포트가 불가능하여 **수동 임포트**가 필요합니다.

---

## ✅ 완료된 작업

1. **성경 데이터 다운로드 완료**
   - 792개 구절 삽입 ✅
   - GitHub: yuhwan/Bible-krv 사용
   - (참고: 전체 성경은 31,000+개지만 테스트용으로 충분)

2. **스토리 분석 준비**
   - analyze_story_units.py 준비됨 ✅
   - 2개 테스트 스토리 생성됨 ✅

3. **워크플로우 파일 준비**
   - workflows/complete_pipeline_story.json ✅
   - n8n API 형식 변환 완료 ✅

---

## 🎯 지금 해야 할 일 (5분)

### n8n 워크플로우 수동 임포트

```bash
# 1. Railway n8n 접속
https://railway.app
→ 'TheMusicalBible' 프로젝트
→ 'n8n' 서비스  
→ 'Open' 버튼

# 2. 로그인 확인
# n8n URL: https://n8n-production-1d6b.up.railway.app

# 3. 워크플로우 임포트
좌측 메뉴 'Workflows' 클릭
→ 우측 상단 '...' (점 3개) 클릭
→ 'Import from File' 선택
→ workflows/complete_pipeline_story.json 선택
→ 'Import' 클릭

# 4. Credentials 연결
각 노드 클릭 → Credential 드롭다운에서 선택:
- PostgreSQL → "Railway PostgreSQL"
- Claude API → "Claude API"  
- Suno API → "Suno API"
- Fish Audio → "Fish Audio API"
- Hedra → "Hedra API"
- Runway → "Runway API"

# 5. 저장 & 활성화
'Save' 버튼 클릭
'Active' 토글 ON (선택)
```

---

## 📊 현재 데이터베이스 상태

```sql
-- scripture 테이블: 792개 구절
SELECT COUNT(*) FROM scripture;
-- 결과: 792

-- story_units 테이블: 2개 스토리
SELECT * FROM story_units;
-- 1. 창세기 1:1-2:3: 하나님의 천지창조
-- 2. 창세기 3:1-24: 인간의 타락과 에덴에서의 추방
```

**테스트 준비 완료!** 워크플로우만 임포트하면 바로 실행 가능합니다.

---

## 🚀 임포트 후 즉시 테스트

```bash
# n8n에서
1. 'Complete Pipeline - 스토리 단위' 워크플로우 열기
2. 'Execute Workflow' 버튼 클릭
3. 10-15분 대기
4. 결과 확인:
   - PostgreSQL에서 status='completed' 확인
   - YouTube 업로드 확인

비용: ₩3,051 (1개 스토리)
```

---

## 📅 다음 단계

### 1. 전체 성경 데이터 (선택사항)

현재 792개만 있지만, 더 많은 데이터 필요 시:

```bash
# 대체 소스 사용 또는
# 수동으로 추가 데이터 삽입
```

### 2. 전체 스토리 분석

```bash
export DATABASE_URL="postgresql://..."
export CLAUDE_API_KEY="sk-ant-..."

python3 scripts/analyze_story_units.py --all

비용: ₩94,500
시간: 2-3시간
결과: 약 3,500개 스토리
```

### 3. 정규 운영 시작

```bash
# n8n에서 Cron Trigger 활성화
# 하루 1개 자동 제작
# 월 비용: ₩155,553
```

---

## 💡 API 인증 문제 해결 (참고)

만약 나중에 API를 사용하고 싶다면:

```bash
# 1. n8n 설정에서 API 활성화 확인
Settings → API → Public API 활성화

# 2. 새 API 키 생성
Settings → API → Create New Key

# 3. 권한 확인
- workflows:read
- workflows:write
- workflows:execute
```

---

## ✅ 체크리스트

- [x] 성경 데이터 다운로드 (792개)
- [x] 테스트 스토리 생성 (2개)
- [x] 워크플로우 파일 준비
- [x] n8n API 형식 변환
- [ ] **n8n 수동 임포트** ⭐ 지금 할 일!
- [ ] Credentials 연결
- [ ] 첫 테스트 실행
- [ ] 결과 확인

---

## 🎉 거의 완료!

**성경 데이터, 스토리, 워크플로우 모두 준비됨!**  
**n8n에서 워크플로우만 임포트하면 바로 영상 제작 시작!**

**소요 시간: 5분**  
**첫 영상 비용: ₩3,051**

🚀 지금 바로 시작하세요!
