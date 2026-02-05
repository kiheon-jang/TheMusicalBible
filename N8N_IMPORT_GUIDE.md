---
date: 2026-01-26
project: 10_Projects/project
tags: ['project']
---
# 🎬 n8n 워크플로우 임포트 가이드 (5분)

**Railway API 연결이 안 되어 수동 임포트가 필요합니다**

---

## 🚀 빠른 시작 (3단계)

### 1️⃣ Railway n8n 접속

```bash
# Railway 대시보드 열기
open https://railway.app

# 또는 직접 접속
# 1. railway.app 접속
# 2. "TheMusicalBible" 프로젝트 클릭
# 3. "n8n" 서비스 클릭
# 4. 우측 "Open" 버튼 클릭
```

**n8n URL 찾기:**
```
Railway Dashboard → Your Project → n8n Service
→ Settings → Domains → Copy URL
```

---

### 2️⃣ 워크플로우 임포트

**n8n 대시보드에서:**

```
1. 좌측 메뉴 "Workflows" 클릭
2. 우측 상단 "..." (점 3개) 클릭
3. "Import from File" 선택
4. workflows/complete_pipeline_story.json 선택
5. "Import" 클릭
```

**파일 위치:**
```
/Users/giheonjang/Documents/project/TMB/workflows/complete_pipeline_story.json
```

---

### 3️⃣ Credentials 연결

워크플로우 임포트 후, 각 노드에 Credential을 연결해야 합니다:

```
노드 이름 → Credential 드롭다운 → 기존 것 선택
```

**필요한 Credentials:**

| 노드 | Credential 이름 | 설정 확인 |
|------|----------------|----------|
| PostgreSQL | Railway PostgreSQL | ✅ 연결 테스트 |
| Claude API | Claude API | ✅ API 키 유효 |
| Fish Audio | Fish Audio API | ✅ 키 확인 |
| Hedra | Hedra API | ✅ 키 확인 |
| Runway | Runway API | ✅ 키 확인 |
| Suno | Suno API | ✅ Custom URL |
| YouTube | YouTube API | ✅ OAuth 연결 |

---

## 📋 상세 가이드

### Step 1: n8n 접속 확인

**n8n 로그인 정보:**
```
Railway에서 n8n 환경변수 확인:
- N8N_BASIC_AUTH_USER
- N8N_BASIC_AUTH_PASSWORD
```

**접속 테스트:**
```bash
# n8n URL 확인
curl -I https://[your-n8n].railway.app

# 응답: 200 OK 확인
```

---

### Step 2: 워크플로우 파일 확인

**현재 프로젝트에 있는 워크플로우:**

```bash
ls -lh workflows/*.json
```

**출력:**
```
complete_pipeline.json         (27K) - 구절 단위 (구버전)
complete_pipeline_story.json   (11K) - 스토리 단위 (신버전) ⭐
```

**사용할 파일: `complete_pipeline_story.json`** ✅

---

### Step 3: Import 프로세스

#### 3.1. n8n 대시보드에서

```
1. 좌측 "Workflows" 클릭
2. 우측 상단 "..." 메뉴
3. "Import from File" 선택
```

#### 3.2. 파일 선택

```
Finder에서:
/Users/giheonjang/Documents/project/TMB/workflows/
→ complete_pipeline_story.json 선택
```

#### 3.3. Import 확인

```
✅ 워크플로우 이름: "complete_pipeline_story"
✅ 노드 개수: ~20개
✅ 상태: Inactive (정상)
```

---

### Step 4: Credentials 설정

**각 노드별로 Credential 연결:**

#### 4.1. PostgreSQL 노드

```
노드명: "PostgreSQL: 스토리 3개 조회"

Credential 설정:
- Host: maglev.proxy.rlwy.net
- Port: 15087
- Database: railway
- User: postgres
- Password: (API_KEYS.txt에서 확인)

✅ "Test Connection" 클릭
```

#### 4.2. Claude API 노드

```
노드명: "Claude: 스토리 프롬프트 생성"

Credential 설정:
- API Key: sk-ant-api03-... (API_KEYS.txt)
- Model: claude-sonnet-4-20250514

✅ Test 실행
```

#### 4.3. Suno API 노드

```
노드명: "Suno: 음악 생성 시작"

HTTP Request 설정:
- URL: https://suno-api-production-ac35.up.railway.app
- Method: POST
- Cookie: (설정 완료 상태)

✅ Webhook 확인
```

#### 4.4. Fish Audio 노드

```
노드명: "Fish Audio: 음성 생성"

Credential 설정:
- API Key: 8024d34fa5b84ee59b74bc5440fd9922

✅ 키 유효성 확인
```

#### 4.5. Hedra 노드

```
노드명: "Hedra: 립싱크 영상"

Credential 설정:
- API Key: sk_hedra_H9RoTOX6... (API_KEYS.txt)

✅ Identity Anchor 확인
```

#### 4.6. Runway 노드

```
노드명: "Runway: 배경 영상 생성"

Credential 설정:
- API Key: key_251946556... (API_KEYS.txt)

✅ Gen-3 모델 확인
```

#### 4.7. YouTube 노드

```
노드명: "YouTube: 업로드"

OAuth 설정:
- Client ID: 1053902423625-... (YOUTUBE_CREDENTIALS.txt)
- Client Secret: GOCSPX-...
- Redirect URI: (Railway n8n URL + /oauth-callback)

✅ OAuth 인증 완료
```

---

### Step 5: 워크플로우 활성화

```
1. 모든 Credentials 연결 확인
2. 우측 상단 "Save" 버튼 클릭
3. "Active" 토글 ON
4. "Execute Workflow" 클릭 → 첫 영상 생성!
```

---

## 🧪 테스트 실행

### 수동 테스트

```
1. complete_pipeline_story 워크플로우 열기
2. 우측 "Execute Workflow" 클릭
3. 실행 로그 확인:
   ✅ PostgreSQL: 스토리 3개 조회
   ✅ Claude: 프롬프트 생성
   ✅ Suno: 음악 생성 시작
   ✅ Fish Audio: 음성 생성
   ✅ Hedra: 립싱크 영상
   ✅ Runway: 배경 영상
   ✅ FFmpeg: 최종 합성
   ✅ YouTube: 업로드

예상 시간: 10-15분
```

### DB 결과 확인

```bash
# 로컬 터미널에서
export DATABASE_URL="postgresql://postgres:cSdtWArmQfsLDSnpuKLoIgxHaRyGREXq@maglev.proxy.rlwy.net:15087/railway"

python3 -c "
import psycopg2
conn = psycopg2.connect('$DATABASE_URL')
cursor = conn.cursor()
cursor.execute('SELECT id, title, status FROM story_units ORDER BY id;')
for row in cursor.fetchall():
    print(f'{row[0]}. {row[1]}: {row[2]}')
"
```

**예상 출력:**
```
1. 하나님의 천지창조: completed
2. 인간의 타락과 에덴에서의 추방: processing
```

---

## 🚨 문제 해결

### 문제 1: Credential이 보이지 않음

**해결:**
```
1. n8n Settings → Credentials
2. "Add Credential" 클릭
3. 해당 서비스 선택
4. API 키 입력 후 저장
```

### 문제 2: PostgreSQL 연결 실패

**해결:**
```bash
# Railway에서 최신 연결 정보 확인
Railway Dashboard → PostgreSQL → Connect Tab
→ Connection URL 복사

# n8n Credential 업데이트
```

### 문제 3: Claude API 404 오류

**해결:**
```
Model 이름 확인:
- 올바름: claude-sonnet-4-20250514
- 잘못됨: claude-3-5-sonnet-20241022

n8n 노드에서 수정:
Claude 노드 → Parameters → Model → 수정
```

### 문제 4: Suno API 타임아웃

**해결:**
```
Suno 노드에서:
- Timeout: 300000 (5분)
- Polling: 활성화
- Retry: 3회

Railway Suno API 서버 상태 확인
```

### 문제 5: YouTube OAuth 오류

**해결:**
```
1. Google Cloud Console
2. OAuth Redirect URI 추가:
   https://[your-n8n].railway.app/oauth-callback
3. n8n에서 재인증
```

---

## 📊 실행 모니터링

### n8n 실행 로그 확인

```
n8n Dashboard → Executions 탭
→ 각 실행 클릭 → 노드별 결과 확인
```

**확인 항목:**
```
✅ 실행 시간 (10-15분 정상)
✅ 각 노드 Success 상태
✅ 최종 YouTube URL 생성
✅ DB status = 'completed'
```

### Railway 로그 확인

```
Railway Dashboard → n8n Service → Logs

필터:
- Error: 오류 확인
- Warning: 경고 확인
- Info: 일반 로그
```

---

## 🎯 자동화 설정 (선택)

### Cron Trigger 활성화

**워크플로우에 Schedule Trigger 추가:**

```
1. "Add Node" 클릭
2. "Schedule Trigger" 선택
3. Cron Expression 설정:
   - 매일 오전 9시: 0 9 * * *
   - 매일 3회: 0 9,15,21 * * *
   - 매 4시간: 0 */4 * * *

4. 연결: Schedule → PostgreSQL 노드
5. Save & Activate
```

**추천 설정 (하루 3개):**
```
Cron: 0 9,15,21 * * *
→ 오전 9시, 오후 3시, 오후 9시

월 비용: $218
완성: 3.2년
```

---

## ✅ 완료 체크리스트

### 임포트 전
- [ ] Railway n8n 접속 확인
- [ ] 로그인 정보 확인
- [ ] 워크플로우 파일 위치 확인

### 임포트 중
- [ ] complete_pipeline_story.json 임포트
- [ ] PostgreSQL Credential 연결
- [ ] Claude API Credential 연결
- [ ] Suno API 설정
- [ ] Fish Audio Credential 연결
- [ ] Hedra Credential 연결
- [ ] Runway Credential 연결
- [ ] YouTube OAuth 연결

### 임포트 후
- [ ] 워크플로우 저장
- [ ] 연결 테스트 (각 Credential)
- [ ] 수동 실행 테스트
- [ ] 실행 로그 확인
- [ ] DB 결과 확인
- [ ] YouTube 업로드 확인

### 자동화 (선택)
- [ ] Cron Trigger 추가
- [ ] 스케줄 설정
- [ ] 활성화
- [ ] 모니터링 설정

---

## 🎉 완료!

**n8n 워크플로우 임포트가 완료되면:**

```
✅ 시스템 가동 준비 완료
✅ 첫 영상 제작 가능
✅ 자동화 시작 가능

→ 이제 실행만 하면 됩니다!
```

**다음 단계:**
1. Execute Workflow 클릭
2. 10-15분 대기
3. YouTube에서 첫 영상 확인
4. 품질 검증
5. 본격 제작 시작!

**모든 준비 완료!** 🚀
