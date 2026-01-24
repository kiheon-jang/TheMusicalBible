# 📈 Phase 2: 고도화 로드맵

**목표**: MVP 완성 후 품질 개선 및 연속성 구현  
**예상 기간**: 1개월  
**전제 조건**: Phase 1 MVP 완성 및 첫 30개 에피소드 제작 완료

---

## 🎯 Phase 2 목표

| 항목 | 목표 | 비고 |
|------|------|------|
| 캐릭터 연속성 | 90% | Hedra Identity Anchor 고도화 |
| 환경 연속성 | 70% | Runway Seed 재사용 |
| 매치 컷 시스템 | 60% | 메타데이터 기반 |
| 통합 영화 제작 | 1편 | 창세기 22-30장 |
| 에러 처리 | 100% | 자동 재시도 및 알림 |

---

## 📋 개선 항목 (우선순위별)

### 🔴 High Priority

#### 1. 에러 처리 및 재시도 로직 (1주)

**목적**: 프로덕션 안정성 확보

**구현 내용**:
```json
// 모든 API 노드에 추가
{
  "continueOnFail": true,
  "retryOnFail": true,
  "maxTries": 3,
  "waitBetweenTries": 5000,
  "onError": "continueRegularOutput"
}
```

**에러 알림 시스템**:
- Telegram Bot 또는 Email 알림
- 에러 로그 DB 저장
- 실패한 구절 자동 재시도 큐

**파일**:
- `workflows/complete_pipeline.json` (모든 API 노드 수정)
- `workflows/error_recovery.json` (새로 생성)

---

#### 2. 환경 연속성 시스템 (1-2주)

**목적**: 같은 장소는 같은 분위기로

**구현 방법**:
```sql
-- DB 스키마 (이미 준비됨)
ALTER TABLE scripture ADD COLUMN runway_seed INTEGER;
ALTER TABLE scripture ADD COLUMN color_palette VARCHAR(50);
ALTER TABLE scripture ADD COLUMN camera_angle VARCHAR(50);

-- 장소 Seed 매핑 테이블
CREATE TABLE location_seeds (
  location_name VARCHAR(100) PRIMARY KEY,
  runway_seed INTEGER NOT NULL,
  color_palette VARCHAR(50),
  camera_angle VARCHAR(50),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO location_seeds VALUES
('ancient desert', 123456, 'warm golden', 'wide shot'),
('Jerusalem temple', 789012, 'cool stone', 'overhead'),
('Mount Sinai', 345678, 'dramatic rocky', 'low angle');
```

**워크플로우 수정**:
```javascript
// complete_pipeline.json - "Runway: 배경 영상 생성" 노드
const location = $json.phase1_location;

// DB에서 Seed 조회
const seedQuery = `
  SELECT runway_seed, color_palette, camera_angle
  FROM location_seeds
  WHERE location_name = $1
`;

const seed = await postgres.query(seedQuery, [location]);

// Runway API 호출 시 Seed 사용
{
  "promptText": $json.phase1_runway_prompt,
  "seed": seed.runway_seed || Math.floor(Math.random() * 1000000),
  "duration": 10
}

// 새로운 Seed는 DB에 저장
if (!seed) {
  INSERT INTO location_seeds (location_name, runway_seed)
  VALUES ($json.phase1_location, newSeed);
}
```

---

#### 3. Hedra Identity Anchor 고도화 (1주)

**목적**: 캐릭터 얼굴 일관성 100% 보장

**구현 방법**:

**Step 1: character_voices 테이블 업데이트**
```sql
-- 이미 준비된 컬럼 활용
ALTER TABLE character_voices 
  ADD COLUMN IF NOT EXISTS hedra_character_id VARCHAR(100),
  ADD COLUMN IF NOT EXISTS last_used_at TIMESTAMP;

-- 인덱스 추가
CREATE INDEX IF NOT EXISTS idx_character_name 
  ON character_voices(character_name);
```

**Step 2: 워크플로우 수정**
```javascript
// complete_pipeline.json - "Hedra: 립싱크 영상 생성" 노드 전에 추가

// 1. DB에서 characterId 조회
const characterQuery = `
  SELECT hedra_character_id
  FROM character_voices
  WHERE character_name = $1
`;

const existingChar = await postgres.query(
  characterQuery, 
  [$json.character_main]
);

// 2-A. 기존 캐릭터 재사용
if (existingChar && existingChar.hedra_character_id) {
  return {
    json: {
      ...$json,
      characterId: existingChar.hedra_character_id,
      isNewCharacter: false
    }
  };
}

// 2-B. 새 캐릭터 생성
else {
  // Hedra API: 캐릭터 생성
  const hedraResponse = await hedra.createCharacter({
    text: $json.phase2_hedra_prompt,
    aspectRatio: "9:16"
  });
  
  const newCharacterId = hedraResponse.characterId;
  
  // DB에 저장
  await postgres.query(`
    INSERT INTO character_voices 
      (character_name, hedra_character_id, last_used_at)
    VALUES ($1, $2, NOW())
    ON CONFLICT (character_name)
    DO UPDATE SET 
      hedra_character_id = $2,
      last_used_at = NOW()
  `, [$json.character_main, newCharacterId]);
  
  return {
    json: {
      ...$json,
      characterId: newCharacterId,
      isNewCharacter: true
    }
  };
}

// 3. Hedra API 호출 (기존/신규 모두)
{
  "characterId": $json.characterId,
  "audioUrl": $json.fish_audio_url,
  "text": $json.phase2_hedra_prompt
}
```

---

#### 4. 매치 컷 메타데이터 시스템 (2주)

**목적**: 에피소드 간 자연스러운 전환

**구현 방법**:

**Step 1: 연속성 메타데이터**
```sql
-- scripture 테이블 (이미 준비됨)
ALTER TABLE scripture 
  ADD COLUMN IF NOT EXISTS prev_episode_id INTEGER,
  ADD COLUMN IF NOT EXISTS next_episode_id INTEGER,
  ADD COLUMN IF NOT EXISTS match_cut_type VARCHAR(50);

-- 외래키 설정
ALTER TABLE scripture
  ADD CONSTRAINT fk_prev_episode 
  FOREIGN KEY (prev_episode_id) REFERENCES scripture(id),
  ADD CONSTRAINT fk_next_episode 
  FOREIGN KEY (next_episode_id) REFERENCES scripture(id);

-- 매치 컷 타입 예시
-- 'location' (같은 장소), 'character' (같은 인물), 
-- 'object' (같은 사물), 'action' (이어지는 동작)
```

**Step 2: 시퀀스 분석 스크립트**
```python
# scripts/analyze_episode_sequence.py

import psycopg2

def analyze_sequence():
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    
    # 연속된 구절 조회
    cur.execute("""
        SELECT id, book_name, chapter, verse, 
               character_main, phase1_location
        FROM scripture
        WHERE status = 'completed'
        ORDER BY book_name, chapter, verse
    """)
    
    episodes = cur.fetchall()
    
    for i in range(len(episodes) - 1):
        current = episodes[i]
        next_ep = episodes[i + 1]
        
        # 매치 컷 타입 결정
        match_type = None
        
        # 같은 장소
        if current[5] == next_ep[5]:
            match_type = 'location'
        
        # 같은 인물
        elif current[4] == next_ep[4]:
            match_type = 'character'
        
        # 연속된 구절
        elif (current[1] == next_ep[1] and 
              current[2] == next_ep[2] and 
              current[3] + 1 == next_ep[3]):
            match_type = 'sequential'
        
        if match_type:
            cur.execute("""
                UPDATE scripture 
                SET next_episode_id = %s,
                    match_cut_type = %s
                WHERE id = %s
            """, (next_ep[0], match_type, current[0]))
            
            cur.execute("""
                UPDATE scripture 
                SET prev_episode_id = %s
                WHERE id = %s
            """, (current[0], next_ep[0]))
    
    conn.commit()
    print("✅ 시퀀스 분석 완료")

if __name__ == "__main__":
    analyze_sequence()
```

**Step 3: 통합 영화 컴파일 스크립트**
```bash
#!/bin/bash
# scripts/compile_movie.sh

BOOK="Genesis"
START_CHAPTER=22
END_CHAPTER=30

echo "🎬 영화 컴파일 시작: $BOOK $START_CHAPTER-$END_CHAPTER장"

# 1. DB에서 에피소드 목록 조회
psql $DATABASE_URL -t -c "
  SELECT video_url 
  FROM scripture 
  WHERE book_name = '$BOOK' 
    AND chapter >= $START_CHAPTER 
    AND chapter <= $END_CHAPTER
    AND status = 'completed'
  ORDER BY chapter, verse
" > episode_list.txt

# 2. FFmpeg concat 파일 생성
while read url; do
  filename=$(basename "$url")
  echo "file '$filename'" >> concat_list.txt
done < episode_list.txt

# 3. 영상 다운로드
while read url; do
  wget -q "$url"
done < episode_list.txt

# 4. FFmpeg 합성
ffmpeg -f concat -safe 0 -i concat_list.txt \
  -c copy \
  -movflags +faststart \
  "output/${BOOK}_Ch${START_CHAPTER}-${END_CHAPTER}_Movie.mp4"

echo "✅ 영화 완성: output/${BOOK}_Ch${START_CHAPTER}-${END_CHAPTER}_Movie.mp4"

# 5. 챕터 마커 추가 (옵션)
# ffmpeg -i input.mp4 -i chapters.txt -map_metadata 1 -codec copy output_with_chapters.mp4
```

---

### 🟡 Medium Priority

#### 5. Google Sheets 분석 연동 (3일)

**목적**: 실시간 성과 모니터링

**구현 내용**:
```javascript
// workflows/complete_pipeline.json - "PostgreSQL: 최종 업데이트" 이후

{
  "id": "google-sheets-update",
  "name": "Google Sheets: 분석 업데이트",
  "type": "n8n-nodes-base.googleSheets",
  "credentials": "googleSheetsOAuth2Api",
  "parameters": {
    "operation": "append",
    "sheetId": "={{ $env.GOOGLE_SHEETS_DOCUMENT_ID }}",
    "range": "Sheet1!A:H",
    "options": {
      "valueInputMode": "USER_ENTERED"
    },
    "dataMode": "autoMapInputData",
    "values": {
      "values": [
        "={{ new Date().toISOString() }}",
        "={{ $json.book_name }}",
        "={{ $json.chapter }}:{{ $json.verse }}",
        "={{ $json.character_main }}",
        "={{ $json.youtube_video_id }}",
        "={{ $json.youtube_views || 0 }}",
        "={{ $json.generation_status }}",
        "={{ $json.total_generation_time }}"
      ]
    }
  }
}
```

---

#### 6. 데이터베이스 인덱스 최적화 (1일)

**파일**: `database/optimize_indexes.sql`

```sql
-- 성능 개선 인덱스
CREATE INDEX IF NOT EXISTS idx_upload_date 
  ON scripture(upload_date DESC);

CREATE INDEX IF NOT EXISTS idx_youtube_views 
  ON scripture(youtube_views DESC);

CREATE INDEX IF NOT EXISTS idx_status_batch 
  ON scripture(status, batch_status);

CREATE INDEX IF NOT EXISTS idx_generation_date 
  ON scripture(generation_date DESC);

-- 복합 인덱스 (자주 조회하는 조건)
CREATE INDEX IF NOT EXISTS idx_status_batch_date 
  ON scripture(status, batch_status, batch_request_date);

CREATE INDEX IF NOT EXISTS idx_book_chapter_verse 
  ON scripture(book_name, chapter, verse);

-- 분석 쿼리 최적화
CREATE INDEX IF NOT EXISTS idx_character_emotion 
  ON scripture(character_main, emotion_primary);

-- VACUUM ANALYZE (정기 실행)
VACUUM ANALYZE scripture;
VACUUM ANALYZE character_voices;
VACUUM ANALYZE youtube_analytics;
```

---

#### 7. API 엔드포인트 검증 및 문서화 (2일)

**목적**: 프로덕션 배포 전 최종 검증

**체크리스트**:

```markdown
## API 엔드포인트 검증

### Claude API
- [ ] Endpoint: https://api.anthropic.com/v1/messages
- [ ] API Key 유효성 확인
- [ ] Rate Limit 확인 (50 req/min)
- [ ] Max Tokens 설정 (1000)

### Fish Audio API
- [ ] Endpoint 확인 (공식 문서 참조)
- [ ] 감정 태그 지원 여부
- [ ] 음성 품질 테스트

### Hedra API
- [ ] Endpoint: https://api.hedra.com/v1/characters
- [ ] Identity Anchor 기능 테스트
- [ ] 9:16 비율 지원 확인
- [ ] 최대 duration 확인

### Runway API
- [ ] Endpoint 확인
- [ ] Seed 파라미터 지원 확인
- [ ] 10초 영상 생성 가능 확인
- [ ] Generation time 측정

### Suno API (Custom Server)
- [ ] Endpoint: https://suno-api-production-ac35.up.railway.app
- [ ] Custom Lyrics 기능 테스트
- [ ] Polling 로직 동작 확인
- [ ] Instrumental/Vocal 모드 전환
```

**테스트 스크립트**:
```bash
# scripts/test_api_endpoints.sh

echo "🧪 API 엔드포인트 테스트 시작"

# Claude API
echo "Testing Claude API..."
curl -X POST https://api.anthropic.com/v1/messages \
  -H "x-api-key: $CLAUDE_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "content-type: application/json" \
  -d '{"model":"claude-3-5-sonnet-20241022","max_tokens":100,"messages":[{"role":"user","content":"Hello"}]}'

# Fish Audio API
echo "Testing Fish Audio API..."
# [실제 엔드포인트로 교체 필요]

# Hedra API
echo "Testing Hedra API..."
# [실제 테스트 스크립트 작성]

# Suno API
echo "Testing Suno API..."
curl -X POST https://suno-api-production-ac35.up.railway.app/generate/description-mode \
  -H "Content-Type: application/json" \
  -d '{"gpt_description_prompt":"Test music","make_instrumental":true}'

echo "✅ 테스트 완료"
```

---

### 🟢 Low Priority (Optional)

#### 8. 다국어 준비 (Phase 3 사전 작업)

**Step 1: 번역 DB 스키마**
```sql
CREATE TABLE scripture_translations (
  id SERIAL PRIMARY KEY,
  scripture_id INTEGER REFERENCES scripture(id),
  language_code VARCHAR(5) NOT NULL,
  korean_text TEXT,
  translated_text TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  UNIQUE(scripture_id, language_code)
);

-- 지원 언어: ko, en, zh, es, ar, pt
```

**Step 2: 번역 API 연동 (나중에)**
- Google Translate API 또는 DeepL
- 성경 전문 번역 DB 활용

---

#### 9. 모니터링 대시보드

**Option 1: Grafana + PostgreSQL**
```yaml
# docker-compose.yml
services:
  grafana:
    image: grafana/grafana
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
    volumes:
      - grafana-data:/var/lib/grafana
```

**Option 2: n8n 워크플로우**
```javascript
// workflows/daily_monitoring.json (이미 존재)
// 매일 AM 9:00 실행
// - 어제 생성된 영상 수
// - YouTube 업로드 성공률
// - 평균 생성 시간
// - API 에러율
// → Telegram 알림
```

---

## 📅 Phase 2 타임라인 (1개월)

### Week 1: 안정성
```
□ 에러 처리 및 재시도 로직
□ API 엔드포인트 검증
□ 데이터베이스 인덱스 최적화
```

### Week 2: 연속성
```
□ 환경 연속성 시스템 (Runway Seed)
□ Hedra Identity Anchor 고도화
□ 캐릭터 얼굴 일관성 테스트
```

### Week 3: 통합
```
□ 매치 컷 메타데이터 시스템
□ 시퀀스 분석 스크립트
□ 에피소드 연결 로직
```

### Week 4: 영화 제작
```
□ 창세기 22-30장 에피소드 완성
□ 통합 영화 컴파일 (60-90분)
□ 챕터 마커 추가
□ 테스트 상영 및 피드백
```

---

## ✅ Phase 2 완료 조건

| 항목 | 목표 | 측정 방법 |
|------|------|-----------|
| 에러율 | < 5% | 100개 에피소드 중 실패 < 5개 |
| 캐릭터 일관성 | > 90% | 사람이 보고 판단 |
| 환경 연속성 | > 70% | 같은 장소 시각적 유사도 |
| 통합 영화 | 1편 | 60분 이상, 챕터 구성 |
| 자동화율 | 100% | 사람 개입 없이 24시간 가동 |

---

## 🚀 Phase 3 Preview

**Phase 2 완료 후 진행 예정**:
- 다국어 자동화 (영어, 중국어, 스페인어)
- 립싱크 재합성 자동화
- 국가별 YouTube 채널 자동 배포
- B2B 라이선스 모델 구축
- VOD 플랫폼 배포

---

## 📊 예상 결과

**Phase 2 완료 시**:
```
✅ 100개 에피소드 자동 생성
✅ 창세기 통합 영화 1편
✅ 에러율 < 5%
✅ 캐릭터 얼굴 일관성 90%+
✅ 완전 자동화 파이프라인

→ 프로덕션 배포 준비 완료! 🎉
```
