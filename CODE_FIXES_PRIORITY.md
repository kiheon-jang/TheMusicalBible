---
date: 2026-01-26
project: 10_Projects/project
tags: ['project']
---
# 🔧 코드 수정 가이드 (우선순위별)

**목표**: 1-2주 내 완전 가동 가능 상태 달성

---

## 🔴 Critical: 1-3일 내 필수 수정

### 1. Evening Generation 워크플로우 수정 (2시간)

**파일**: `workflows/evening_generation.json`

#### Step 1: Suno API 엔드포인트 수정

**수정 전**:
```json
{
  "id": "suno-music",
  "name": "Suno: 배경음악 생성",
  "type": "n8n-nodes-base.httpRequest",
  "parameters": {
    "url": "https://api.suno.ai/v1/generate"  ❌
  }
}
```

**수정 후**:
```json
{
  "id": "suno-music",
  "name": "Suno: 배경음악 생성",
  "type": "n8n-nodes-base.httpRequest",
  "parameters": {
    "method": "POST",
    "url": "https://suno-api-production-ac35.up.railway.app/generate/description-mode",
    "sendBody": true,
    "bodyParameters": {
      "parameters": [
        {
          "name": "gpt_description_prompt",
          "value": "={{ $json.music_prompt }}"
        },
        {
          "name": "make_instrumental",
          "value": true
        },
        {
          "name": "mv",
          "value": "chirp-v3-5"
        }
      ]
    }
  }
}
```

#### Step 2: Suno Polling 로직 추가

Suno는 즉시 완성되지 않으므로, Polling이 필요합니다.

**추가 노드 1: Wait for Suno**
```json
{
  "id": "wait-suno",
  "name": "Wait: 2분 대기",
  "type": "n8n-nodes-base.wait",
  "parameters": {
    "amount": 120,
    "unit": "seconds"
  }
}
```

**추가 노드 2: Check Suno Status**
```json
{
  "id": "check-suno-status",
  "name": "Suno: 상태 확인",
  "type": "n8n-nodes-base.httpRequest",
  "parameters": {
    "method": "GET",
    "url": "https://suno-api-production-ac35.up.railway.app/feed/={{ $json.clip_ids[0] }}"
  }
}
```

**추가 노드 3: Loop Until Complete**
```json
{
  "id": "loop-until-complete",
  "name": "If: 완료 확인",
  "type": "n8n-nodes-base.if",
  "parameters": {
    "conditions": {
      "boolean": [
        {
          "value1": "={{ $json.status }}",
          "value2": "complete"
        }
      ]
    }
  },
  "routing": {
    "true": ["download-suno"],
    "false": ["wait-suno"]  // 루프
  }
}
```

**또는 간단하게**: 이미 구현된 `suno_with_polling.json` 워크플로우를 사용하세요!

**추가 노드 4: Execute Workflow**
```json
{
  "id": "call-suno-polling",
  "name": "Execute: Suno Polling",
  "type": "n8n-nodes-base.executeWorkflow",
  "parameters": {
    "workflowId": "{{ $workflow.getWorkflowByName('Suno 음악 생성 (Polling)').id }}",
    "source": "parameter",
    "options": {
      "waitForCompletion": true
    }
  }
}
```

---

#### Step 3: 파일 다운로드 노드 추가

각 API 호출 후에 파일을 다운로드하는 노드를 추가합니다.

**Suno 다운로드**:
```json
{
  "id": "download-suno",
  "name": "Download: Suno 음악",
  "type": "n8n-nodes-base.httpRequest",
  "parameters": {
    "method": "GET",
    "url": "={{ $json.audio_url }}",
    "responseFormat": "file",
    "options": {
      "output": {
        "fileName": "{{ $json.episode_id }}_music.mp3"
      }
    }
  }
}
```

**Fish Audio 다운로드**:
```json
{
  "id": "download-fish",
  "name": "Download: Fish 음성",
  "type": "n8n-nodes-base.httpRequest",
  "parameters": {
    "method": "GET",
    "url": "={{ $json.audio_url }}",
    "responseFormat": "file",
    "options": {
      "output": {
        "fileName": "{{ $json.episode_id }}_voice.mp3"
      }
    }
  }
}
```

**Hedra 다운로드**:
```json
{
  "id": "download-hedra",
  "name": "Download: Hedra 영상",
  "type": "n8n-nodes-base.httpRequest",
  "parameters": {
    "method": "GET",
    "url": "={{ $json.video_url }}",
    "responseFormat": "file",
    "options": {
      "output": {
        "fileName": "{{ $json.episode_id }}_video.mp4"
      }
    }
  }
}
```

---

#### Step 4: SQLite → PostgreSQL 노드 변경

모든 SQLite 노드를 PostgreSQL로 변경합니다.

**수정 전**:
```json
{
  "type": "n8n-nodes-base.sqlite",
  "credentials": {
    "sqlite": {
      "id": "sqlite-credentials",
      "name": "SQLite DB"
    }
  }
}
```

**수정 후**:
```json
{
  "type": "n8n-nodes-base.postgres",
  "credentials": {
    "postgres": {
      "id": "postgresql-credentials",
      "name": "Railway PostgreSQL"
    }
  }
}
```

**쿼리 문법 수정**:
```sql
-- SQLite:
INSERT OR IGNORE INTO scripture ...
INSERT OR REPLACE INTO youtube_analytics ...

-- PostgreSQL:
INSERT INTO scripture ... ON CONFLICT (id) DO NOTHING
INSERT INTO youtube_analytics ... ON CONFLICT (scripture_id, date) DO UPDATE SET ...
```

---

### 2. 모든 워크플로우에 SQLite → PostgreSQL 변경 (1시간)

**대상 파일**:
- `workflows/morning_batch.json`
- `workflows/evening_generation.json`
- `workflows/daily_monitoring.json`

**자동 변경 스크립트**:
```bash
cd /Users/giheonjang/Documents/project/TMB/workflows

# 백업
cp morning_batch.json morning_batch.json.backup
cp evening_generation.json evening_generation.json.backup
cp daily_monitoring.json daily_monitoring.json.backup

# 일괄 변경
for file in *.json; do
  # SQLite → Postgres 노드 타입 변경
  sed -i '' 's/"n8n-nodes-base\.sqlite"/"n8n-nodes-base.postgres"/g' "$file"
  
  # Credentials ID 변경
  sed -i '' 's/"sqlite-credentials"/"postgresql-credentials"/g' "$file"
  sed -i '' 's/"SQLite DB"/"Railway PostgreSQL"/g' "$file"
  
  # INSERT OR IGNORE → ON CONFLICT
  sed -i '' 's/INSERT OR IGNORE/INSERT/g' "$file"
  sed -i '' 's/INSERT OR REPLACE/INSERT/g' "$file"
done

echo "✅ 변경 완료! n8n에서 임포트하세요."
```

---

### 3. API 키 보안 강화 (30분)

#### Step 1: .gitignore 업데이트

**파일**: `.gitignore`

```gitignore
# API Keys & Credentials
API_KEYS.txt
*_CREDENTIALS.txt
YOUTUBE_CREDENTIALS.txt
*.env
.env.*

# Railway Secrets
railway.json

# Database
*.db
*.sqlite
*.sqlite3

# Sensitive Docs
QUICK_CREDENTIALS_SETUP.md
CONNECTION_STATUS.md
```

#### Step 2: Git 히스토리에서 API 키 제거

```bash
# Git 히스토리에서 민감한 파일 완전 제거
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch API_KEYS.txt" \
  --prune-empty --tag-name-filter cat -- --all

git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch QUICK_CREDENTIALS_SETUP.md" \
  --prune-empty --tag-name-filter cat -- --all

# 강제 푸시 (주의!)
git push origin --force --all
```

#### Step 3: API 키 재발급

모든 API 키를 재발급하세요 (이미 노출되었으므로):

1. **Claude API**: https://console.anthropic.com/settings/keys
2. **Hedra API**: Hedra 대시보드
3. **Fish Audio API**: Fish Audio 설정
4. **Runway API**: Runway 설정

#### Step 4: Railway 환경 변수 업데이트

```bash
railway variables set CLAUDE_API_KEY="새_키"
railway variables set HEDRA_API_KEY="새_키"
railway variables set FISH_AUDIO_API_KEY="새_키"
railway variables set RUNWAY_API_KEY="새_키"
```

---

## 🟡 High: 1주일 내 권장 수정

### 4. Claude Batch API 구현 (3시간)

**문서 요구사항**:
```
Morning (AM 2:00): Batch 요청 전송 → batch_id 저장
Evening (PM 2:00): Batch 결과 조회 → 프롬프트 가져오기
```

#### Morning Batch 수정

**파일**: `workflows/morning_batch.json`

**수정 전**:
```json
{
  "id": "claude-batch-request",
  "parameters": {
    "url": "https://api.anthropic.com/v1/messages"  ❌
  }
}
```

**수정 후**:
```json
{
  "id": "claude-batch-request",
  "name": "Claude: Batch 요청",
  "type": "n8n-nodes-base.httpRequest",
  "parameters": {
    "method": "POST",
    "url": "https://api.anthropic.com/v1/messages/batches",
    "authentication": "predefinedCredentialType",
    "nodeCredentialType": "anthropicApi",
    "sendHeaders": true,
    "headerParameters": {
      "parameters": [
        {
          "name": "anthropic-version",
          "value": "2023-06-01"
        }
      ]
    },
    "sendBody": true,
    "bodyParameters": {
      "parameters": [
        {
          "name": "requests",
          "value": "={{ $json.batch_requests }}"
        }
      ]
    }
  }
}
```

**Batch 요청 데이터 준비**:
```javascript
// Batch 요청 데이터 준비 노드:
const items = $input.all();
const batchRequests = items.map(item => ({
  custom_id: `scripture_${item.json.id}`,
  params: {
    model: "claude-3-5-sonnet-20241022",
    max_tokens: 1000,
    messages: [{
      role: "user",
      content: `성경 구절: ${item.json.korean_text}\n...`
    }]
  }
}));

return [{
  json: {
    batch_requests: batchRequests
  }
}];
```

**batch_id 저장**:
```sql
-- SQLite Update 노드:
UPDATE scripture 
SET batch_request_id = $1,
    batch_status = 'waiting',
    batch_request_date = NOW()
WHERE id IN ($2)
```

#### Evening Generation 수정

**Batch 결과 조회**:
```json
{
  "id": "claude-batch-results",
  "name": "Claude: Batch 결과 조회",
  "type": "n8n-nodes-base.httpRequest",
  "parameters": {
    "method": "GET",
    "url": "https://api.anthropic.com/v1/messages/batches/={{ $json.batch_request_id }}",
    "authentication": "predefinedCredentialType",
    "nodeCredentialType": "anthropicApi"
  }
}
```

---

### 5. Hedra 30초 직접 생성 (1시간)

**현재 문제**:
```bash
# FFmpeg로 5초 → 30초 확장 (품질 저하)
setpts=6.0*PTS  ❌
```

**해결 방법**: Hedra API에 30초 요청

**Hedra API 문서 확인 필요**:
```json
{
  "id": "hedra-video",
  "parameters": {
    "url": "https://api.hedra.com/v1/...",
    "bodyParameters": {
      "duration": 30,  // ✅ 30초로 변경
      "quality": "1080p"
    }
  }
}
```

**만약 Hedra가 5초만 지원한다면**:

**대안 1: Loop 반복**
```bash
# FFmpeg: 5초를 6번 반복
ffmpeg -stream_loop 5 -i input.mp4 \
  -t 30 -c copy output.mp4
```

**대안 2: Frame Interpolation**
```bash
# FFmpeg: 프레임 보간으로 부드럽게
ffmpeg -i input.mp4 \
  -filter:v "minterpolate='fps=24:mi_mode=mci:mc_mode=aobmc:me_mode=bidir:vsbmc=1',setpts=6.0*PTS" \
  output.mp4
```

---

### 6. Identity Anchor 이미지 업로드 (2시간)

#### Step 1: 캐릭터 이미지 생성

**DALL-E 3로 10개 캐릭터 이미지 생성**:
```python
import openai

characters = [
    "abraham", "david", "moses", "eve", "jacob",
    "joseph", "mary", "jesus", "peter", "paul"
]

for char in characters:
    prompt = f"A cinematic portrait of {char.capitalize()} from the Bible, facing forward, serious expression, dramatic lighting, 4K, photorealistic"
    
    response = openai.Image.create(
        model="dall-e-3",
        prompt=prompt,
        size="1024x1024",
        quality="hd"
    )
    
    image_url = response.data[0].url
    # 다운로드 및 저장
```

#### Step 2: Google Cloud Storage 업로드

```bash
# Google Cloud Storage 버킷 생성
gsutil mb gs://tmb-characters

# 이미지 업로드 (공개)
gsutil cp ./characters/*.jpg gs://tmb-characters/
gsutil acl ch -u AllUsers:R gs://tmb-characters/*.jpg

# URL 확인
echo "https://storage.googleapis.com/tmb-characters/abraham.jpg"
```

#### Step 3: 데이터베이스 업데이트

```sql
UPDATE character_voices 
SET identity_anchor_image_url = 'https://storage.googleapis.com/tmb-characters/abraham.jpg'
WHERE character_name = 'abraham';

-- 반복 (10개 캐릭터)
```

---

## 🟢 Medium: 개선 권장 (필수 아님)

### 7. 에러 처리 및 재시도 로직 (1시간)

**모든 API 노드에 추가**:
```json
{
  "continueOnFail": true,
  "retryOnFail": true,
  "maxTries": 3,
  "waitBetweenTries": 5000,
  "onError": "continueRegularOutput"
}
```

**에러 알림 노드 추가**:
```json
{
  "id": "error-notification",
  "name": "Telegram: 에러 알림",
  "type": "n8n-nodes-base.telegram",
  "parameters": {
    "chatId": "YOUR_CHAT_ID",
    "text": "⚠️ 에러 발생: {{ $json.error }}"
  }
}
```

---

### 8. Google Sheets 문서 ID 설정 (10분)

#### Step 1: Google Sheets 생성

1. https://sheets.google.com 접속
2. 새 스프레드시트 생성
3. 이름: "The Musical Bible Analytics"
4. 시트 이름: "YouTube Analytics"

#### Step 2: 문서 ID 복사

URL에서 문서 ID 복사:
```
https://docs.google.com/spreadsheets/d/1AbC...XyZ/edit
                                       ^^^^^^^^^^^ 이 부분
```

#### Step 3: Railway 환경 변수 설정

```bash
railway variables set GOOGLE_SHEETS_DOCUMENT_ID="1AbC...XyZ"
```

---

### 9. 데이터베이스 인덱스 추가 (5분)

**파일**: `database/init_postgresql.sql`

```sql
-- 추가 인덱스
CREATE INDEX IF NOT EXISTS idx_upload_date ON scripture(upload_date DESC);
CREATE INDEX IF NOT EXISTS idx_youtube_views ON scripture(youtube_views DESC);
CREATE INDEX IF NOT EXISTS idx_status_batch ON scripture(status, batch_status);
CREATE INDEX IF NOT EXISTS idx_generation_date ON scripture(generation_date DESC);

-- 복합 인덱스 (자주 조회하는 조건)
CREATE INDEX IF NOT EXISTS idx_status_batch_date 
  ON scripture(status, batch_status, batch_request_date);
```

---

## ✅ 수정 완료 체크리스트

### 🔴 Critical (1-3일)
- [ ] Suno API 엔드포인트 수정
- [ ] Suno Polling 로직 추가
- [ ] 파일 다운로드 노드 추가 (Suno, Fish, Hedra, Runway)
- [ ] SQLite → PostgreSQL 노드 변경 (모든 워크플로우)
- [ ] API 키 보안 강화 (.gitignore, 재발급)

### 🟡 High (1주일)
- [ ] Claude Batch API 구현
- [ ] Hedra 30초 직접 생성 (또는 대안)
- [ ] Identity Anchor 이미지 생성 & 업로드

### 🟢 Medium (개선 권장)
- [ ] 에러 처리 및 재시도 로직
- [ ] Google Sheets 문서 ID 설정
- [ ] 데이터베이스 인덱스 추가

---

## 📞 다음 단계

1. **Critical 수정** (1-3일):
   - 모든 API 엔드포인트 검증
   - 워크플로우 수정 및 임포트
   - 보안 강화

2. **End-to-End 테스트** (1일):
   - Morning Batch → Evening Generation → Daily Monitoring
   - 전체 파이프라인 1회 수동 실행
   - 에러 로그 확인

3. **자동화 활성화** (이후):
   - Cron 트리거 활성화
   - 일일 모니터링 시작
   - 수익 분석 시작

---

**🎯 목표 달성 일정**:
- **Day 1-3**: Critical 수정
- **Day 4**: 테스트 실행
- **Day 5-7**: High 우선순위 개선
- **Day 8+**: 자동화 가동 및 모니터링

**🚀 화이팅!**
