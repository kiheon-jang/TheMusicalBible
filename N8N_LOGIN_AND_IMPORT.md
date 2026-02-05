---
date: 2026-01-26
project: 10_Projects/project
tags: ['project']
---
# 🎯 n8n 로그인 & 워크플로우 임포트 가이드 (상세)

## 📋 로그인 정보

```
URL: https://n8n-production-1d6b.up.railway.app
이메일: xaqwer@gmail.com
비밀번호: Wkdrlgjs2@
```

---

## ✅ 완료된 작업

1. **성경 데이터 다운로드 완료** ✅
   - 792개 구절 삽입됨
   - DB 준비 완료

2. **스토리 생성 완료** ✅
   - 2개 테스트 스토리 생성
   - 바로 영상 제작 가능

3. **워크플로우 파일 준비** ✅
   - `complete_pipeline_story.json` 준비됨

---

## 🚀 지금 할 일 (10분)

### Step 1: n8n 로그인 (2분)

```bash
# 브라우저에서 접속
https://n8n-production-1d6b.up.railway.app

# 로그인
이메일: xaqwer@gmail.com
비밀번호: Wkdrlgjs2@
```

---

### Step 2: 워크플로우 임포트 (3분)

**임포트 방법:**

1. **좌측 메뉴에서 'Workflows' 클릭**

2. **우측 상단 '...' (점 3개) 클릭**
   - 또는 'Add Workflow' 버튼 옆

3. **'Import from File' 선택**

4. **파일 선택**
   ```
   파일 경로:
   /Users/giheonjang/Documents/project/TMB/workflows/complete_pipeline_story.json
   ```

5. **'Import' 버튼 클릭**

---

### Step 3: Credentials 연결 (5분)

워크플로우가 임포트되면 각 노드에 Credential을 연결해야 합니다.

#### 📊 PostgreSQL 노드

**노드명:** "PostgreSQL: 스토리 3개 조회 (순차)"

```
Credential: PostgreSQL

설정:
- Host: maglev.proxy.rlwy.net
- Port: 15087
- Database: railway
- User: postgres
- Password: cSdtWArmQfsLDSnpuKLoIgxHaRyGREXq
- SSL Mode: Require

✅ 'Test Connection' 클릭하여 확인
```

#### 🤖 Claude API 노드

**노드명:** "Claude: 스토리 프롬프트 생성"

```
Credential: Claude API (HTTP Header Auth)

설정:
- Header Name: x-api-key
- Header Value: (API_KEYS.txt 파일 참조)

또는

Credential Type: Generic Credential Type
- API Key: (위의 키 입력)
```

#### 🎵 Suno API 노드

**노드명:** "Suno: 음악 생성 시작"

```
Credential: HTTP Request (Custom)

설정:
- Authentication: None (Cookie 사용)
- Base URL: https://suno-api-production-ac35.up.railway.app
```

#### 🎤 Fish Audio 노드

**노드명:** "Fish Audio: 음성 생성"

```
Credential: HTTP Header Auth

설정:
- Header Name: Authorization
- Header Value: 8024d34fa5b84ee59b74bc5440fd9922
```

#### 👤 Hedra 노드

**노드명:** "Hedra: 립싱크 영상"

```
Credential: HTTP Header Auth

설정:
- Header Name: x-api-key
- Header Value: sk_hedra_H9RoTOX6ZvWtnctjIJ0ThjIA1gTWGa9F8Onc9EZFpupYkTiZaVzCCDZGJ51OMCvq
```

#### 🎬 Runway 노드

**노드명:** "Runway: 배경 영상 생성"

```
Credential: HTTP Header Auth

설정:
- Header Name: Authorization
- Header Value: Bearer key_251946556723bdf0b9794eb0296b8f0be1407a79073afd64642b3b454cf653c04d4b9af33116e05c493e9401174d4ed25ba1ce690c51c451a934cd4fb2a62332
```

---

### Step 4: 저장 & 테스트 실행

1. **'Save' 버튼 클릭** (우측 상단)

2. **(선택) 'Active' 토글 ON**
   - Cron이 활성화되어 매일 오전 3시에 자동 실행

3. **수동 테스트 실행**
   ```
   'Execute Workflow' 버튼 클릭
   → 10-15분 대기
   → 실행 로그 확인
   ```

---

## 📊 실행 확인

### n8n 실행 로그

```
우측 'Executions' 탭 클릭
→ 최신 실행 클릭
→ 각 노드별 결과 확인
```

**확인 사항:**
- ✅ PostgreSQL: 스토리 3개 조회 성공
- ✅ Claude: 프롬프트 생성 성공
- ✅ Suno: 음악 생성 시작
- ✅ Fish Audio: 음성 생성
- ✅ Hedra: 립싱크 영상
- ✅ Runway: 배경 영상
- ✅ FFmpeg: 합성 완료
- ✅ YouTube: 업로드 성공

### 데이터베이스 확인

```sql
-- 로컬 터미널에서
python3 -c "
import psycopg2
conn = psycopg2.connect('postgresql://postgres:cSdtWArmQfsLDSnpuKLoIgxHaRyGREXq@maglev.proxy.rlwy.net:15087/railway')
cursor = conn.cursor()
cursor.execute('SELECT id, title, status FROM story_units ORDER BY id;')
for row in cursor.fetchall():
    print(f'{row[0]}. {row[1]}: {row[2]}')
"
```

**예상 결과:**
```
1. 하나님의 천지창조: completed
2. 인간의 타락과 에덴에서의 추방: processing
```

---

## 🚨 문제 해결

### 로그인 실패

```
1. 비밀번호 재확인: Wkdrlgjs2@
2. Railway 접속 확인
3. n8n 서비스 상태 확인
```

### Credential 연결 실패

```
각 API 키 재확인:
- API_KEYS.txt 참고
- 복사할 때 공백 없이
```

### 실행 중 에러

```
Executions 탭에서 에러 메시지 확인:
- Claude API: 모델명 확인 (claude-sonnet-4-20250514)
- Suno: Custom URL 확인
- Runway: 크레딧 잔액 확인
- Hedra: 크레딧 잔액 확인
```

---

## 💰 비용

```
첫 테스트 (1개 영상): ₩3,051
정규 운영 (하루 1개): ₩155,553/월
```

---

## ✅ 완료 체크리스트

### 로그인
- [ ] n8n 접속
- [ ] 이메일/비밀번호 입력
- [ ] 로그인 성공

### 임포트
- [ ] Workflows 메뉴
- [ ] Import from File
- [ ] complete_pipeline_story.json 선택
- [ ] Import 완료

### Credentials
- [ ] PostgreSQL 연결
- [ ] Claude API 연결
- [ ] Suno API 연결
- [ ] Fish Audio 연결
- [ ] Hedra 연결
- [ ] Runway 연결

### 실행
- [ ] Save 클릭
- [ ] Execute Workflow
- [ ] 실행 로그 확인
- [ ] DB 결과 확인
- [ ] YouTube 업로드 확인

---

## 🎉 완료 후

**첫 영상 제작 완료!**

다음 단계:
1. 영상 품질 확인
2. 프로세스 최적화
3. 정규 운영 시작 (Cron 활성화)
4. 채널 성장 모니터링

**월 ₩155,553으로 하루 1개씩 제작!**  
**9.7년 만에 전체 성경 완성!** 🚀

---

## 📞 빠른 참조

```
n8n URL: https://n8n-production-1d6b.up.railway.app
로그인: xaqwer@gmail.com / Wkdrlgjs2@
워크플로우: workflows/complete_pipeline_story.json
API 키: API_KEYS.txt 참고
DB 정보: PostgreSQL (Railway)
```

**10분이면 완료됩니다!** 지금 바로 시작하세요! 🎬
