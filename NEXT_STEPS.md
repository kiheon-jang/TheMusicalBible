---
date: 2026-02-01
project: 10_Projects/project
tags: ['project']
---
# 🎯 The Musical Bible - 다음 단계 (하루 1개 업로드)

**결정:** 하루 1개 업로드 (월 ₩155,553)

---

## ✅ 현재 상태

```
✅ PostgreSQL DB: 연결 완료
✅ 테이블: story_units, verse_to_story 생성
✅ 스크립트: analyze_story_units.py 완성
✅ 워크플로우: complete_pipeline_story.json 준비
✅ 테스트 스토리: 2개 생성

⚠️  성경 데이터: 5개만 (31,102개 필요)
⚠️  스토리 분석: 2개만 (3,500개 필요)
❌ n8n: 임포트 대기
```

---

## 🎯 지금 해야 할 일 (30분)

### 1️⃣ n8n 워크플로우 임포트 (10분) ⭐ 최우선

```bash
# Railway 접속
https://railway.app
→ 프로젝트 'TheMusicalBible'
→ 'n8n' 서비스
→ 'Open' 버튼

# 임포트
1. 좌측 'Workflows'
2. 우측 '...' → 'Import from File'
3. workflows/complete_pipeline_story.json
4. Credentials 연결
5. Save & Activate
```

**상세 가이드:** `[[N8N_IMPORT_GUIDE]].md`

---

### 2️⃣ 성경 데이터 확보 (20분)

**문제:** GitHub URL이 404로 작동 안 함

**해결 방법 A - API 사용 (추천):**
```bash
# Bible API 사용
# 예: https://bible-api.com
# 또는 성서공회 API
```

**해결 방법 B - 수동 입력:**
```bash
# 테스트용으로 창세기만 먼저
# 나중에 전체 확보
```

**해결 방법 C - 대체 GitHub 저장소:**
```bash
# yuhwan/Bible-krv
# sungcheolkim78/py_kbible
```

---

## 📅 이후 단계

### 오늘 (임포트 후)

```bash
# 첫 테스트 영상 제작
1. n8n에서 'Execute Workflow' 클릭
2. 10-15분 대기
3. DB 확인:
   SELECT * FROM story_units WHERE status='completed';
4. YouTube 확인

비용: ₩3,051 (1개)
```

### 내일

```bash
# 성경 데이터 확보 및 분석
1. 전체 성경 데이터 삽입
2. 스토리 분석 실행:
   python3 scripts/analyze_story_units.py --all
   
비용: ₩94,500 (분석)
시간: 2-3시간
결과: 3,500개 스토리
```

### 이번 주

```bash
# 정규 운영 시작
1. n8n Cron 활성화 (하루 1개)
2. 모니터링
3. 품질 확인
4. 프로세스 최적화

비용: ₩155,553/월
```

---

## 💰 비용 재확인

### 월간 비용 (하루 1개)
```
구독료:         ₩105,300
추가 사용량:    ₩50,253
━━━━━━━━━━━━━━━━━━━━━
총:             ₩155,553/월
```

### 초기 투자
```
성경 분석:      ₩94,500 (1회)
첫 테스트:      ₩3,051 (1개)
━━━━━━━━━━━━━━━━━━━━━
총:             ₩97,551
```

---

## 🚨 주의사항

### Runway 크레딧 부족
```
Standard 플랜: 월 625 크레딧
필요: 2,400 크레딧 (30개)
→ 22개는 매달 추가 구매 (₩24,000)

대안:
1. 격일 1개 (월 15개) → 구독 범위 내
2. Runway Pro ($28/월) → 1,500 크레딧
```

---

## 📞 문의/문제

### 성경 데이터 404
- 대체 소스 찾는 중
- 필요 시 수동 입력도 가능

### n8n 접속 문제
- Railway 로그인 확인
- n8n URL 확인

### API 키 문제
- API_KEYS.txt 확인
- Credential 재설정

---

## ✅ 완료 체크리스트

### 즉시 (오늘)
- [ ] n8n 워크플로우 임포트
- [ ] Credentials 연결
- [ ] 첫 테스트 영상 제작
- [ ] 결과 확인

### 이번 주
- [ ] 성경 데이터 확보
- [ ] 전체 스토리 분석
- [ ] 정규 운영 시작
- [ ] 비용 문서 업데이트

### 이번 달
- [ ] 30개 영상 제작
- [ ] YouTube 최적화
- [ ] 구독자 100명
- [ ] 프로세스 안정화

---

**지금 바로 시작하세요!** 🚀

1. n8n 임포트 (10분)
2. 테스트 실행 (15분)
3. 결과 확인 (5분)

**30분이면 첫 영상 완성!**
