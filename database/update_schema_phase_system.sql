-- The Musical Bible - DB 스키마 업데이트
-- 3단계 시네마틱 구조 추가
-- 실행 방법: Railway PostgreSQL 콘솔에서 실행

-- 1. Phase 1 (Scripture Context) 필드 추가
ALTER TABLE scripture ADD COLUMN IF NOT EXISTS phase1_shot_type VARCHAR(50);
ALTER TABLE scripture ADD COLUMN IF NOT EXISTS phase1_location VARCHAR(255);
ALTER TABLE scripture ADD COLUMN IF NOT EXISTS phase1_runway_prompt TEXT;
ALTER TABLE scripture ADD COLUMN IF NOT EXISTS phase1_duration INTEGER DEFAULT 8;

-- 2. Phase 2 (Atmosphere & Tension) 필드 추가
ALTER TABLE scripture ADD COLUMN IF NOT EXISTS phase2_character_state TEXT;
ALTER TABLE scripture ADD COLUMN IF NOT EXISTS phase2_hedra_prompt TEXT;
ALTER TABLE scripture ADD COLUMN IF NOT EXISTS phase2_duration INTEGER DEFAULT 10;

-- 3. Phase 3 (Aria & Grand Finale) 필드 추가
ALTER TABLE scripture ADD COLUMN IF NOT EXISTS phase3_vocal_lyrics TEXT;
ALTER TABLE scripture ADD COLUMN IF NOT EXISTS phase3_suno_prompt TEXT;
ALTER TABLE scripture ADD COLUMN IF NOT EXISTS phase3_visual_climax TEXT;
ALTER TABLE scripture ADD COLUMN IF NOT EXISTS phase3_duration INTEGER DEFAULT 12;

-- 4. 캐릭터 관리 필드 추가
ALTER TABLE scripture ADD COLUMN IF NOT EXISTS fish_emotion_tags VARCHAR(255);

-- 5. 환경 연속성 필드 추가
ALTER TABLE scripture ADD COLUMN IF NOT EXISTS runway_seed VARCHAR(255);
ALTER TABLE scripture ADD COLUMN IF NOT EXISTS camera_angle VARCHAR(50);
ALTER TABLE scripture ADD COLUMN IF NOT EXISTS color_palette VARCHAR(255);

-- 6. 시네마틱 통합 필드 추가 (Phase 2에서 사용)
ALTER TABLE scripture ADD COLUMN IF NOT EXISTS prev_episode_id INTEGER;
ALTER TABLE scripture ADD COLUMN IF NOT EXISTS next_episode_id INTEGER;
ALTER TABLE scripture ADD COLUMN IF NOT EXISTS transition_type VARCHAR(50);
ALTER TABLE scripture ADD COLUMN IF NOT EXISTS sound_bridge_url TEXT;

-- 7. 인덱스 추가 (성능 최적화)
CREATE INDEX IF NOT EXISTS idx_location ON scripture(phase1_location);
CREATE INDEX IF NOT EXISTS idx_prev_episode ON scripture(prev_episode_id);
CREATE INDEX IF NOT EXISTS idx_next_episode ON scripture(next_episode_id);

-- 8. 기존 데이터 마이그레이션 (visual_prompt가 있는 경우)
UPDATE scripture 
SET phase1_runway_prompt = visual_prompt,
    phase3_vocal_lyrics = vocal_prompt,
    phase3_suno_prompt = music_prompt
WHERE visual_prompt IS NOT NULL 
  AND phase1_runway_prompt IS NULL;

-- 9. 검증 쿼리 (추가된 컬럼 확인)
SELECT column_name, data_type, character_maximum_length
FROM information_schema.columns
WHERE table_name = 'scripture'
  AND column_name LIKE 'phase%'
ORDER BY column_name;

-- 완료 메시지
SELECT 'DB 스키마 업데이트 완료! 3단계 시네마틱 구조가 추가되었습니다.' AS status;
