# ⚡ 빠른 설치 가이드 (5분)

## 🎯 한 줄 요약

**이 명령어 하나로 모든 설정 완료!**

```bash
./scripts/setup_story_mode.sh
```

---

## 📋 사전 준비 (1분)

### 1. Railway 연결 문자열 가져오기

```bash
# Railway 대시보드 접속
# 1. https://railway.app/dashboard
# 2. 프로젝트 클릭
# 3. PostgreSQL 서비스 클릭
# 4. 'Connect' 탭 클릭
# 5. 'Postgres Connection URL' 복사

# 예시:
# postgresql://postgres:abc123@containers-us-west-123.railway.app:5432/railway
```

### 2. Claude API 키 가져오기

```bash
# Claude 대시보드 접속
# 1. https://console.anthropic.com/
# 2. API Keys 메뉴
# 3. 'Create Key' 클릭
# 4. 키 복사

# 예시:
# sk-ant-api03-abc123...
```

### 3. 환경 변수 설정

```bash
# 터미널에서 실행
export DATABASE_URL="postgresql://postgres:password@host:5432/railway"
export CLAUDE_API_KEY="sk-ant-api03-..."

# 영구 저장 (선택)
echo 'export DATABASE_URL="..."' >> ~/.zshrc
echo 'export CLAUDE_API_KEY="..."' >> ~/.zshrc
source ~/.zshrc
```

---

## 🚀 설치 실행 (3분)

```bash
cd /Users/giheonjang/Documents/project/TMB

# 이 명령어 하나로 모든 것이 자동 설치됩니다!
./scripts/setup_story_mode.sh
```

**자동으로 실행되는 것**:
1. ✅ story_units 테이블 생성
2. ✅ Python 패키지 설치
3. ✅ 창세기 1-5장 스토리 분석
4. ✅ 결과 확인

**예상 소요 시간**: 3분

---

## 🎬 n8n 워크플로우 임포트 (1분)

**자동화 불가 - 수동으로 해야 합니다:**

```bash
# 1. Railway n8n 대시보드 열기
open https://[your-n8n-url].railway.app

# 2. 워크플로우 임포트
# - 좌측 메뉴 'Workflows' 클릭
# - 'Import' 버튼 클릭
# - workflows/complete_pipeline_story.json 선택
# - 'Save' 클릭

# 3. Credentials 연결
# - 각 노드의 Credentials 드롭다운에서 기존 것 선택
# - PostgreSQL: Railway PostgreSQL
# - Claude API: Claude API
# - Fish Audio: Fish Audio API
# - Hedra: Hedra API
# - Runway: Runway API
# - Suno: Suno API
# - YouTube: YouTube API

# 4. 'Save' 클릭
```

---

## ✅ 설치 확인

### 자동 확인 (스크립트 완료 시)

```
📊 통계:
  - 총 스토리: 8 개
  - 총 구절: 93 개
  - 평균 길이: 75 초

🎉 설치 완료!
```

### 수동 확인 (선택)

```bash
# DB 확인
psql "$DATABASE_URL" -c "SELECT COUNT(*) FROM story_units;"

# 스토리 목록 확인
psql "$DATABASE_URL" -c "SELECT title FROM story_units LIMIT 5;"
```

---

## 🧪 테스트 실행

### n8n에서 테스트

```
1. Railway n8n 접속
2. complete_pipeline_story 워크플로우 열기
3. 'Execute Workflow' 버튼 클릭
4. 실행 로그 확인
5. DB에서 결과 확인:
   psql "$DATABASE_URL" -c "SELECT * FROM story_units WHERE status='completed';"
```

---

## 📊 추가 분석 (선택)

### 창세기 전체 분석 (100개 스토리)

```bash
python3 scripts/analyze_story_units.py --genesis

# 소요 시간: 30분
# 비용: ~$2
```

### 전체 성경 분석 (3,500개 스토리)

```bash
python3 scripts/analyze_story_units.py --all

# 소요 시간: 2-3시간
# 비용: ~$70
```

---

## 🚨 문제 해결

### 오류: "DATABASE_URL not set"

```bash
# 환경 변수 다시 설정
export DATABASE_URL="postgresql://..."
echo $DATABASE_URL  # 확인
```

### 오류: "CLAUDE_API_KEY not set"

```bash
# API 키 다시 설정
export CLAUDE_API_KEY="sk-ant-..."
echo $CLAUDE_API_KEY  # 확인 (앞 10자만 표시)
```

### 오류: "psql: command not found"

```bash
# PostgreSQL 클라이언트 설치
brew install postgresql
```

### 오류: "ModuleNotFoundError: anthropic"

```bash
# Python 패키지 재설치
pip install anthropic psycopg2-binary requests
```

### 오류: Claude API 429 (Rate Limit)

```bash
# 5분 대기 후 재실행
sleep 300
./scripts/setup_story_mode.sh
```

---

## 💰 비용 안내

### 설치 비용 (1회)

```
테스트 분석 (창세기 1-5장): $0.50
창세기 전체: $2
전체 성경: $70
```

### 제작 비용 (지속)

```
스토리당: $2.26
전체 3,500개: $7,910

vs 구절 단위 (31,102개): $70,290
절감: $62,380 (89%!)
```

---

## 🎯 다음 단계

### 즉시 (오늘)
```
✅ setup_story_mode.sh 실행
✅ n8n 워크플로우 임포트
✅ 테스트 실행 1회
```

### 이번 주
```
□ 창세기 전체 분석 (--genesis)
□ 테스트 영상 10개 제작
□ 품질 검증
```

### 다음 달
```
□ 전체 성경 분석 (--all)
□ Cron 활성화 (매일 3개)
□ YouTube 채널 성장
□ 1년 내 완성!
```

---

## 🎉 설치 완료 후

**축하합니다!** 🎉

이제 스토리 모드가 활성화되었습니다:

- ✅ 31,102개 → 3,500개 영상
- ✅ $70,290 → $7,910 (89% 절감)
- ✅ 8.5년 → 1년 (88% 단축)
- ✅ 설교 구조로 자연스러운 콘텐츠

**1년 내 완성 가능합니다!** 🚀

---

## 📞 도움이 필요하면

1. 로그 확인: `cat setup_story_mode.log`
2. DB 상태: `psql "$DATABASE_URL" -c "\dt"`
3. 스토리 개수: `psql "$DATABASE_URL" -c "SELECT COUNT(*) FROM story_units;"`

**모든 준비 완료!** 이제 제작만 시작하면 됩니다! 🎬
