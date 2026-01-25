# 🔧 빠른 Credential 연결 가이드

## 📊 현재 상태

```
✅ PostgreSQL: 통과!
✅ book_order 테이블: 생성 완료
✅ 스토리 데이터: 14개 준비됨
❌ Claude Credential: 연결 필요!
```

---

## 🎯 2분 안에 해결하는 방법

### n8n에서 직접 연결 (가장 빠름!)

**URL:** https://n8n-production-1d6b.up.railway.app/workflow/QoMfESYU0FCalwdb

### Step 1: Claude 노드 열기 (30초)
1. 워크플로우에서 `Claude: 스토리 프롬프트 생성` 노드 더블클릭
2. 우측 패널 열림

### Step 2: Credential 생성 (1분)
1. `Credential for Anthropic API` 드롭다운 클릭
2. `+ Create New` 클릭
3. API Key 입력:
   ```
   (API_KEYS.txt 또는 환경변수 사용)
   ```
4. `Save` 클릭

### Step 3: 워크플로우 저장 (10초)
- 우측 상단 `Save` 버튼 클릭

### Step 4: 실행! (10초)
- `Execute Workflow` 버튼 클릭!

---

## 🚀 실행 후 예상 결과

### 성공 시:
```
✅ PostgreSQL: 스토리 3개 조회
✅ Claude: 프롬프트 생성
✅ 스토리 데이터 업데이트
→ 다음 단계 (Suno, Fish, Hedra, Runway) 준비 완료!
```

### 예상 시간:
- 프롬프트 생성: 10-20초
- 3개 스토리 처리: 30-60초

### 예상 비용:
- Claude API: ~₩100 (3개 스토리)

---

## 📝 다음 단계

프롬프트 생성 성공 후:
1. Suno, Fish Audio, Hedra, Runway credentials 연결
2. 첫 전체 영상 테스트
3. YouTube 업로드

---

## 💡 또는 제가 계속 시도할까요?

브라우저 자동화로 credential 생성을 계속 시도할 수 있습니다.
단, UI에서 직접 하는 것이 확실하고 빠릅니다 (2분).

**어떻게 하시겠습니까?**
