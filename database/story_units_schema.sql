-- The Musical Bible (TMB) - 스토리 단위 스키마
-- 설교 단위(페리코페)로 성경을 그룹핑

-- 스토리 단위 테이블
CREATE TABLE IF NOT EXISTS story_units (
  id SERIAL PRIMARY KEY,
  book_name VARCHAR(255) NOT NULL,
  verses_range VARCHAR(50) NOT NULL,  -- 예: "1:1-31", "3:1-24"
  title VARCHAR(255) NOT NULL,        -- 예: "천지 창조", "선악과 사건"
  verse_count INTEGER NOT NULL,       -- 포함된 구절 수
  key_theme TEXT,                     -- 핵심 주제
  main_characters JSONB,              -- ["아담", "하와"]
  story_arc TEXT,                     -- 스토리 구조 설명
  estimated_duration_sec INTEGER,     -- 예상 영상 길이 (60-180초)
  narrative_structure JSONB,          -- 기승전결 구조
  
  -- 3단계 시네마틱 구조 (Phase 1, 2, 3)
  phase1_shot_type VARCHAR(50),
  phase1_location VARCHAR(255),
  phase1_runway_prompt TEXT,
  phase1_duration INTEGER DEFAULT 30,
  
  phase2_character_state TEXT,
  phase2_character_description TEXT,
  phase2_hedra_prompt TEXT,
  phase2_duration INTEGER DEFAULT 30,
  
  phase3_vocal_lyrics TEXT,
  phase3_suno_prompt TEXT,
  phase3_visual_climax TEXT,
  phase3_duration INTEGER DEFAULT 60,
  
  -- 통합 프롬프트
  visual_prompt TEXT,
  vocal_prompt TEXT,
  music_prompt TEXT,
  emotion_values TEXT,
  fish_emotion_tags VARCHAR(255),
  
  -- API 결과 URL
  suno_url TEXT,
  suno_audio_path TEXT,
  fish_url TEXT,
  fish_audio_path TEXT,
  hedra_url TEXT,
  hedra_video_path TEXT,
  runway_url TEXT,
  runway_video_path TEXT,
  
  -- 최종 영상
  final_video_path TEXT,
  thumbnail_path TEXT,
  
  -- YouTube 정보
  youtube_url TEXT,
  youtube_video_id VARCHAR(255),
  youtube_views INTEGER DEFAULT 0,
  youtube_likes INTEGER DEFAULT 0,
  youtube_comments INTEGER DEFAULT 0,
  
  -- 타임스탬프
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  generation_date TIMESTAMP,
  upload_date TIMESTAMP,
  
  -- 상태
  status VARCHAR(50) DEFAULT 'pending',
  processing_error TEXT,
  
  UNIQUE(book_name, verses_range)
);

-- 구절 → 스토리 매핑 테이블
CREATE TABLE IF NOT EXISTS verse_to_story (
  id SERIAL PRIMARY KEY,
  story_unit_id INTEGER REFERENCES story_units(id) ON DELETE CASCADE,
  scripture_id INTEGER REFERENCES scripture(id) ON DELETE CASCADE,
  order_in_story INTEGER,  -- 스토리 내 순서
  
  UNIQUE(story_unit_id, scripture_id)
);

-- 인덱스
CREATE INDEX IF NOT EXISTS idx_story_status ON story_units(status);
CREATE INDEX IF NOT EXISTS idx_story_book ON story_units(book_name);
CREATE INDEX IF NOT EXISTS idx_story_created ON story_units(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_verse_story ON verse_to_story(story_unit_id);

-- 통계 뷰
CREATE OR REPLACE VIEW story_stats AS
SELECT 
  status,
  COUNT(*) as count,
  SUM(verse_count) as total_verses,
  AVG(estimated_duration_sec) as avg_duration
FROM story_units
GROUP BY status;

SELECT '✅ 스토리 단위 스키마 생성 완료!' as status;
