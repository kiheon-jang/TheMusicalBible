# 🔍 API 엔드포인트 검증 체크리스트

**목표**: 모든 API의 실제 엔드포인트 확인 및 테스트

---

## 📝 검증 방법

### 1. 공식 문서 확인
각 API의 공식 문서에서 엔드포인트와 요청/응답 형식을 확인합니다.

### 2. Postman/Curl 테스트
실제 API 호출을 테스트하여 작동을 확인합니다.

### 3. n8n에서 테스트
n8n HTTP Request 노드로 직접 테스트합니다.

---

## 🎵 1. Suno API

### ✅ 현재 구현 (비공식 API)

**엔드포인트**: `https://suno-api-production-ac35.up.railway.app`

**상태**: ✅ 배포 완료 및 작동 확인

**사용 가능한 엔드포인트**:

#### 1.1 음악 생성 (Description Mode)
```bash
POST /generate/description-mode

# Request Body:
{
  "gpt_description_prompt": "Fear emotion for Abraham's dilemma. Sparse string orchestration with tremolo. Minor key, 60 BPM. Divine but harsh. No lyrics, instrumental only.",
  "make_instrumental": true,
  "mv": "chirp-v3-5"
}

# Response:
{
  "clip_ids": ["abc123-def456-..."],
  "status": "processing"
}
```

#### 1.2 생성 상태 확인
```bash
GET /feed/{clip_id}

# Response (생성 중):
{
  "id": "abc123",
  "status": "processing",
  "audio_url": null
}

# Response (완료):
{
  "id": "abc123",
  "status": "complete",
  "audio_url": "https://cdn.suno.ai/.../audio.mp3",
  "video_url": "https://cdn.suno.ai/.../video.mp4",
  "metadata": {...}
}
```

#### 1.3 크레딧 확인
```bash
GET /get_credits

# Response:
{
  "credits_left": 500,
  "period": "monthly",
  "monthly_limit": 2500,
  "monthly_usage": 2000
}
```

### 🔧 n8n 워크플로우 권장 구조

**Option 1: Execute Workflow 사용 (권장)**
```json
{
  "id": "call-suno-polling",
  "name": "Execute: Suno 음악 생성",
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

**Option 2: Inline 구현**
```json
// 1. POST /generate/description-mode
// 2. Wait 30초
// 3. Loop: GET /feed/{clip_id} (최대 10회)
// 4. If status == "complete" → Download audio_url
```

### ✅ 검증 체크리스트

- [x] Suno API 서버 배포 완료
- [x] `/generate/description-mode` 엔드포인트 확인
- [x] `/feed/{clip_id}` 엔드포인트 확인
- [ ] n8n에서 전체 Polling 로직 테스트
- [ ] Suno 쿠키 만료 시 재설정 프로세스 확인

---

## 🎬 2. Hedra API

### ⚠️ 확인 필요

**공식 웹사이트**: https://www.hedra.com/

**문제**: 공식 API 문서를 찾을 수 없음

### 🔍 확인 사항

1. **Hedra API Key 확인**:
   ```
   API Key: sk_hedra_H9RoTO...
   ```
   - Hedra 대시보드에서 API 섹션 확인
   - API 문서 링크 찾기

2. **엔드포인트 추정**:
   ```bash
   POST https://api.hedra.com/v1/characters
   또는
   POST https://api.hedra.com/v1/generate
   ```

3. **Identity Anchor 사용 방법**:
   ```json
   {
     "prompt": "Abraham in fear, dramatic lighting",
     "identity_anchor": "https://storage.googleapis.com/.../abraham.jpg",
     "duration": 5,  // 또는 30?
     "quality": "1080p"
   }
   ```

### 🧪 테스트 방법

#### Curl 테스트:
```bash
curl -X POST https://api.hedra.com/v1/characters \
  -H "X-API-Key: sk_hedra_H9RoTO..." \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Test character generation",
    "duration": 5,
    "quality": "1080p"
  }'
```

#### n8n 테스트:
```json
{
  "name": "Test Hedra API",
  "nodes": [
    {
      "type": "n8n-nodes-base.httpRequest",
      "parameters": {
        "method": "POST",
        "url": "https://api.hedra.com/v1/...",
        "authentication": "predefinedCredentialType",
        "nodeCredentialType": "httpHeaderAuth",
        "sendBody": true,
        "bodyParameters": {
          "parameters": [
            {
              "name": "prompt",
              "value": "Test"
            }
          ]
        }
      },
      "credentials": {
        "httpHeaderAuth": {
          "id": "hedra-api-credentials"
        }
      }
    }
  ]
}
```

### ✅ 검증 체크리스트

- [ ] Hedra API 공식 문서 찾기
- [ ] 실제 엔드포인트 URL 확인
- [ ] Identity Anchor 파라미터 이름 확인
- [ ] Duration 최대값 확인 (5초? 30초?)
- [ ] 응답 형식 확인 (즉시 URL? 비동기?)
- [ ] n8n에서 테스트 실행

---

## 🐟 3. Fish Audio API

### ⚠️ 확인 필요

**공식 웹사이트**: https://fish.audio/

**API Key**: `8024d34fa5b8...`

### 🔍 확인 사항

1. **공식 API 문서**:
   - https://fish.audio/docs
   - 또는 대시보드에서 API 섹션 확인

2. **엔드포인트 추정**:
   ```bash
   POST https://api.fish.audio/v1/tts
   또는
   POST https://api.fish.audio/v1/synthesis
   ```

3. **요청 형식**:
   ```json
   {
     "text": "아브라함이여, 네 아들을 가져와라",
     "voice_id": "abraham_voice_id_1",
     "language": "ko",
     "emotion": {
       "fear": 0.9,
       "trembling": 0.8,
       "reverence": 0.7
     }
   }
   ```

### 🧪 테스트 방법

#### Curl 테스트:
```bash
curl -X POST https://api.fish.audio/v1/tts \
  -H "Authorization: Bearer 8024d34fa5b8..." \
  -H "Content-Type: application/json" \
  -d '{
    "text": "테스트 음성 합성",
    "language": "ko"
  }'
```

### ✅ 검증 체크리스트

- [ ] Fish Audio API 공식 문서 찾기
- [ ] 실제 엔드포인트 URL 확인
- [ ] 한국어 지원 확인 (`language: "ko"`)
- [ ] 감정 파라미터 지원 확인
- [ ] Voice ID 형식 확인
- [ ] 응답 형식 확인 (MP3 URL? Binary?)
- [ ] n8n에서 테스트 실행

---

## 🎥 4. Runway API

### ⚠️ 확인 필요

**공식 웹사이트**: https://runwayml.com/

**API Key**: `key_251946556723bdf...`

### 🔍 확인 사항

1. **공식 API 문서**:
   - https://docs.runwayml.com/
   - Gen-2 vs Gen-3 확인

2. **엔드포인트 추정**:
   ```bash
   POST https://api.runwayml.com/v1/generations
   또는
   POST https://api.runwayml.com/v1/gen2
   ```

3. **요청 형식**:
   ```json
   {
     "prompt": "Desert landscape at sunset, cinematic",
     "duration": 30,
     "mode": "gen2"
   }
   ```

### 🧪 테스트 방법

#### Curl 테스트:
```bash
curl -X POST https://api.runwayml.com/v1/generations \
  -H "Authorization: Bearer key_251946..." \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Test video generation",
    "duration": 10
  }'
```

### ✅ 검증 체크리스트

- [ ] Runway API 공식 문서 찾기
- [ ] Gen-2 vs Gen-3 차이 확인
- [ ] 실제 엔드포인트 URL 확인
- [ ] Duration 최대값 확인 (10초? 30초?)
- [ ] 비용 계산 (30초 영상당 비용)
- [ ] 응답 형식 확인 (비동기? Polling 필요?)
- [ ] n8n에서 테스트 실행

---

## 🤖 5. Claude API

### ✅ 확인 완료

**공식 문서**: https://docs.anthropic.com/

**상태**: ✅ API 키 유효 (크레딧 부족)

### Batch API 엔드포인트

#### 5.1 Batch 요청 생성
```bash
POST https://api.anthropic.com/v1/messages/batches

Headers:
  x-api-key: sk-ant-api03-...
  anthropic-version: 2023-06-01
  content-type: application/json

Body:
{
  "requests": [
    {
      "custom_id": "scripture_1",
      "params": {
        "model": "claude-3-5-sonnet-20241022",
        "max_tokens": 1000,
        "messages": [
          {
            "role": "user",
            "content": "성경 구절: ..."
          }
        ]
      }
    }
  ]
}

Response:
{
  "id": "msgbatch_01ABC...",
  "type": "message_batch",
  "processing_status": "in_progress",
  "request_counts": {
    "processing": 3,
    "succeeded": 0,
    "errored": 0,
    "canceled": 0,
    "expired": 0
  },
  "created_at": "2024-01-01T00:00:00Z",
  "expires_at": "2024-01-02T00:00:00Z"
}
```

#### 5.2 Batch 결과 조회
```bash
GET https://api.anthropic.com/v1/messages/batches/{batch_id}

Response:
{
  "id": "msgbatch_01ABC...",
  "processing_status": "ended",
  "request_counts": {
    "succeeded": 3,
    "errored": 0
  },
  "results_url": "https://api.anthropic.com/.../results.jsonl"
}
```

#### 5.3 Batch 결과 다운로드
```bash
GET https://api.anthropic.com/v1/messages/batches/{batch_id}/results

Response (JSONL):
{"custom_id":"scripture_1","result":{"type":"succeeded","message":{...}}}
{"custom_id":"scripture_2","result":{"type":"succeeded","message":{...}}}
{"custom_id":"scripture_3","result":{"type":"succeeded","message":{...}}}
```

### ✅ 검증 체크리스트

- [x] Claude API 공식 문서 확인
- [x] API 키 유효성 확인
- [ ] 크레딧 충전 (최소 $5)
- [ ] Batch API 테스트 실행
- [ ] n8n에서 Batch 워크플로우 구현

---

## 📺 6. YouTube Data API v3

### ✅ 확인 완료

**공식 문서**: https://developers.google.com/youtube/v3

**상태**: ✅ OAuth2 설정 완료

### 사용 엔드포인트

#### 6.1 영상 업로드
```bash
POST https://www.googleapis.com/upload/youtube/v3/videos?part=snippet,status

Headers:
  Authorization: Bearer {access_token}
  Content-Type: video/mp4

Body (Multipart):
  - Metadata (JSON)
  - Video File (Binary)
```

**n8n 노드**: `n8n-nodes-base.youtube` (내장)

#### 6.2 Analytics 조회
```bash
GET https://youtubeanalytics.googleapis.com/v2/reports?
  ids=channel==MINE&
  startDate=2024-01-01&
  endDate=2024-01-31&
  metrics=views,estimatedMinutesWatched,likes,comments&
  dimensions=video&
  filters=video=={video_id}

Response:
{
  "columnHeaders": [...],
  "rows": [
    ["video_id", 1234, 5678, 100, 50]
  ]
}
```

### ✅ 검증 체크리스트

- [x] YouTube OAuth2 설정 완료
- [x] YouTube Data API 활성화
- [ ] n8n에서 업로드 테스트
- [ ] n8n에서 Analytics 조회 테스트

---

## 🗄️ 7. PostgreSQL (Railway)

### ✅ 확인 완료

**연결 정보**:
```
Host: maglev.proxy.rlwy.net
Port: 15087
Database: railway
User: postgres
Password: cSdtW... (Railway에서 확인)
```

**상태**: ✅ 연결 가능

### ✅ 검증 체크리스트

- [x] Railway PostgreSQL 배포 완료
- [x] 데이터베이스 스키마 생성
- [x] 초기 데이터 삽입 (10개 캐릭터)
- [ ] n8n에서 연결 테스트
- [ ] 쿼리 실행 테스트

---

## 📊 전체 검증 상태

| API | 상태 | 우선순위 | 예상 시간 |
|-----|------|---------|----------|
| Suno | ✅ 완료 | - | - |
| Claude | ⚠️ 크레딧 필요 | 🔴 High | 10분 |
| Hedra | ❌ 확인 필요 | 🔴 Critical | 1시간 |
| Fish Audio | ❌ 확인 필요 | 🔴 Critical | 1시간 |
| Runway | ❌ 확인 필요 | 🟡 Medium | 1시간 |
| YouTube | ✅ 완료 | - | - |
| PostgreSQL | ✅ 완료 | - | - |

**총 예상 시간**: 3-4시간

---

## 🔧 검증 워크플로우 템플릿

### n8n 테스트 워크플로우

**파일**: `workflows/test_all_apis.json`

```json
{
  "name": "API 전체 테스트",
  "nodes": [
    {
      "id": "manual-trigger",
      "name": "Manual Trigger",
      "type": "n8n-nodes-base.manualTrigger"
    },
    {
      "id": "test-claude",
      "name": "Test: Claude API",
      "type": "n8n-nodes-base.httpRequest",
      "parameters": {
        "url": "https://api.anthropic.com/v1/messages",
        "method": "POST",
        "sendBody": true,
        "bodyParameters": {
          "model": "claude-3-5-sonnet-20241022",
          "max_tokens": 100,
          "messages": [{
            "role": "user",
            "content": "Hello"
          }]
        }
      }
    },
    {
      "id": "test-hedra",
      "name": "Test: Hedra API",
      "type": "n8n-nodes-base.httpRequest",
      "parameters": {
        "url": "https://api.hedra.com/v1/...",
        "method": "POST"
      }
    },
    {
      "id": "test-fish",
      "name": "Test: Fish Audio API",
      "type": "n8n-nodes-base.httpRequest",
      "parameters": {
        "url": "https://api.fish.audio/v1/...",
        "method": "POST"
      }
    },
    {
      "id": "test-runway",
      "name": "Test: Runway API",
      "type": "n8n-nodes-base.httpRequest",
      "parameters": {
        "url": "https://api.runwayml.com/v1/...",
        "method": "POST"
      }
    },
    {
      "id": "test-suno",
      "name": "Test: Suno API",
      "type": "n8n-nodes-base.httpRequest",
      "parameters": {
        "url": "https://suno-api-production-ac35.up.railway.app/get_credits",
        "method": "GET"
      }
    },
    {
      "id": "test-postgresql",
      "name": "Test: PostgreSQL",
      "type": "n8n-nodes-base.postgres",
      "parameters": {
        "operation": "executeQuery",
        "query": "SELECT COUNT(*) FROM scripture"
      }
    }
  ]
}
```

---

## 📝 다음 단계

1. **각 API 공식 문서 찾기** (1시간)
   - Hedra, Fish Audio, Runway 문서 링크 확인
   - 엔드포인트 및 요청/응답 형식 파악

2. **Curl/Postman 테스트** (1시간)
   - 각 API에 실제 요청 전송
   - 응답 형식 확인
   - 에러 메시지 확인

3. **n8n 테스트 워크플로우 실행** (1시간)
   - 위의 템플릿 임포트
   - 각 노드 개별 실행
   - 성공/실패 로그 확인

4. **워크플로우 수정** (1시간)
   - 실제 엔드포인트로 수정
   - 요청/응답 형식 맞추기
   - 재테스트

---

**🎯 완료 시점**: 모든 API가 n8n에서 정상 작동 확인

**다음 문서**: `CODE_FIXES_PRIORITY.md` (수정 가이드)
