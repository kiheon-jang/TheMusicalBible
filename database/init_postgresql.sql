-- The Musical Bible (TMB) - PostgreSQL 데이터베이스 스키마
-- Railway PostgreSQL용

-- 테이블 1: scripture (성경 데이터)
CREATE TABLE IF NOT EXISTS scripture (
  -- 기본 정보
  id SERIAL PRIMARY KEY,
  book_name VARCHAR(255) NOT NULL,
  chapter INTEGER NOT NULL,
  verse INTEGER NOT NULL,
  korean_text TEXT NOT NULL,
  
  -- 캐릭터 정보
  character_main VARCHAR(100),
  character_secondary VARCHAR(100),
  
  -- 감정 분석 (0.0-1.0 범위)
  emotion_primary VARCHAR(50),
  emotion_secondary VARCHAR(50),
  fear_level REAL DEFAULT 0.0,
  resolve_level REAL DEFAULT 0.0,
  confusion_level REAL DEFAULT 0.0,
  fatigue_level REAL DEFAULT 0.0,
  grief_level REAL DEFAULT 0.0,
  hope_level REAL DEFAULT 0.0,
  
  -- 생성 프롬프트 (Claude에서 생성)
  visual_prompt TEXT,
  vocal_prompt TEXT,
  music_prompt TEXT,
  emotion_values TEXT,  -- JSON 형식
  
  -- Batch 처리 상태
  batch_request_id VARCHAR(255),
  batch_status VARCHAR(50) DEFAULT 'pending',
  batch_response TEXT,
  
  -- 개별 API 결과 URL
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
  youtube_watch_time_hours REAL DEFAULT 0.0,
  youtube_revenue REAL DEFAULT 0.0,
  youtube_likes INTEGER DEFAULT 0,
  youtube_comments INTEGER DEFAULT 0,
  
  -- 타임스탐프
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  batch_request_date TIMESTAMP,
  generation_date TIMESTAMP,
  upload_date TIMESTAMP,
  
  -- 상태
  status VARCHAR(50) DEFAULT 'pending',
  processing_error TEXT,
  
  -- 모니터링
  notes TEXT
);

-- 인덱스 생성
CREATE INDEX IF NOT EXISTS idx_status ON scripture(status);
CREATE INDEX IF NOT EXISTS idx_batch_status ON scripture(batch_status);
CREATE INDEX IF NOT EXISTS idx_character ON scripture(character_main);
CREATE INDEX IF NOT EXISTS idx_emotion ON scripture(emotion_primary);
CREATE INDEX IF NOT EXISTS idx_book_chapter_verse ON scripture(book_name, chapter, verse);

-- 테이블 2: character_voices (캐릭터 설정)
CREATE TABLE IF NOT EXISTS character_voices (
  id SERIAL PRIMARY KEY,
  character_name VARCHAR(100) NOT NULL UNIQUE,
  
  -- Fish Audio 음성 ID
  fish_audio_voice_id VARCHAR(255),
  
  -- Hedra Identity Anchor
  identity_anchor_s3_path TEXT,
  identity_anchor_image_url TEXT,
  identity_anchor_local_path TEXT,
  
  -- 기본 감정
  default_emotion VARCHAR(50),
  default_fear REAL DEFAULT 0.0,
  default_resolve REAL DEFAULT 0.5,
  default_confusion REAL DEFAULT 0.0,
  default_fatigue REAL DEFAULT 0.0,
  
  -- 메타데이터
  age_description VARCHAR(255),
  gender VARCHAR(20),
  description TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP
);

-- 테이블 3: api_usage_log (API 사용 로그)
CREATE TABLE IF NOT EXISTS api_usage_log (
  id SERIAL PRIMARY KEY,
  api_name VARCHAR(100) NOT NULL,
  scripture_id INTEGER REFERENCES scripture(id),
  request_type VARCHAR(50),
  request_url TEXT,
  request_body TEXT,
  response_status INTEGER,
  response_body TEXT,
  duration_ms INTEGER,
  cost_usd REAL DEFAULT 0.0,
  error_message TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_api_name ON api_usage_log(api_name);
CREATE INDEX IF NOT EXISTS idx_api_created ON api_usage_log(created_at);

-- 테이블 4: youtube_analytics (YouTube 통계)
CREATE TABLE IF NOT EXISTS youtube_analytics (
  id SERIAL PRIMARY KEY,
  scripture_id INTEGER REFERENCES scripture(id),
  date DATE NOT NULL,
  views INTEGER DEFAULT 0,
  watch_time_hours REAL DEFAULT 0.0,
  revenue REAL DEFAULT 0.0,
  likes INTEGER DEFAULT 0,
  comments INTEGER DEFAULT 0,
  shares INTEGER DEFAULT 0,
  subscribers_gained INTEGER DEFAULT 0,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  UNIQUE(scripture_id, date)
);

CREATE INDEX IF NOT EXISTS idx_youtube_date ON youtube_analytics(date);

-- 테이블 5: workflow_execution_log (워크플로우 실행 로그)
CREATE TABLE IF NOT EXISTS workflow_execution_log (
  id SERIAL PRIMARY KEY,
  workflow_name VARCHAR(255) NOT NULL,
  execution_id VARCHAR(255),
  status VARCHAR(50),
  start_time TIMESTAMP,
  end_time TIMESTAMP,
  duration_seconds INTEGER,
  error_message TEXT,
  metadata TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_workflow_name ON workflow_execution_log(workflow_name);
CREATE INDEX IF NOT EXISTS idx_workflow_status ON workflow_execution_log(status);

-- 초기 캐릭터 데이터 삽입
INSERT INTO character_voices (character_name, fish_audio_voice_id, identity_anchor_image_url, default_emotion, default_fear, default_resolve, age_description, gender, description) VALUES
  ('abraham', 'abraham_voice_id_1', 'https://example.com/characters/abraham.jpg', 'reverent_fear', 0.8, 0.9, '137세의 할아버지', 'male', '아브라함 - 믿음의 조상'),
  ('david', 'david_voice_id_1', 'https://example.com/characters/david.jpg', 'kingly_resolve', 0.3, 0.95, '젊은 왕', 'male', '다윗 - 이스라엘의 왕'),
  ('moses', 'moses_voice_id_1', 'https://example.com/characters/moses.jpg', 'prophetic_awe', 0.6, 0.9, '나이 든 선지자', 'male', '모세 - 율법을 받은 선지자'),
  ('eve', 'eve_voice_id_1', 'https://example.com/characters/eve.jpg', 'innocent_curiosity', 0.2, 0.5, '젊은 여성', 'female', '하와 - 최초의 여인'),
  ('jacob', 'jacob_voice_id_1', 'https://example.com/characters/jacob.jpg', 'struggling_resolve', 0.5, 0.7, '중년 남성', 'male', '야곱 - 이스라엘의 조상'),
  ('joseph', 'joseph_voice_id_1', 'https://example.com/characters/joseph.jpg', 'wise_forgiveness', 0.3, 0.9, '중년 남성', 'male', '요셉 - 꿈을 해석한 총리'),
  ('mary', 'mary_voice_id_1', 'https://example.com/characters/mary.jpg', 'humble_acceptance', 0.4, 0.95, '젊은 여성', 'female', '마리아 - 예수의 어머니'),
  ('jesus', 'jesus_voice_id_1', 'https://example.com/characters/jesus.jpg', 'compassionate_authority', 0.1, 1.0, '30대 남성', 'male', '예수 - 구세주'),
  ('peter', 'peter_voice_id_1', 'https://example.com/characters/peter.jpg', 'passionate_zeal', 0.4, 0.8, '중년 남성', 'male', '베드로 - 열두 제자 중 하나'),
  ('paul', 'paul_voice_id_1', 'https://example.com/characters/paul.jpg', 'fervent_conviction', 0.3, 0.95, '중년 남성', 'male', '바울 - 복음을 전한 사도')
ON CONFLICT (character_name) DO NOTHING;
