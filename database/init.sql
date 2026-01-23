-- The Musical Bible (TMB) - SQLite 데이터베이스 스키마
-- 초기화 스크립트

-- 테이블 1: scripture (성경 데이터)
CREATE TABLE IF NOT EXISTS scripture (
  -- 기본 정보
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  book_name TEXT NOT NULL,              -- Genesis, Exodus, ...
  chapter INTEGER NOT NULL,
  verse INTEGER NOT NULL,
  korean_text TEXT NOT NULL,            -- 한글 개역개정 본문
  
  -- 캐릭터 정보
  character_main TEXT,                  -- Abraham, David, Moses, Eve, Jacob
  character_secondary TEXT,
  
  -- 감정 분석 (0.0-1.0 범위)
  emotion_primary TEXT,                 -- fear, joy, sorrow, awe, anger, hope
  emotion_secondary TEXT,
  fear_level REAL DEFAULT 0.0,
  resolve_level REAL DEFAULT 0.0,
  confusion_level REAL DEFAULT 0.0,
  fatigue_level REAL DEFAULT 0.0,
  grief_level REAL DEFAULT 0.0,
  hope_level REAL DEFAULT 0.0,
  
  -- 생성 프롬프트 (Claude에서 생성)
  visual_prompt TEXT,                   -- Hedra/Runway용
  vocal_prompt TEXT,                    -- Fish Audio용
  music_prompt TEXT,                    -- Suno용
  emotion_values TEXT,                  -- JSON 형식: {"fear":0.8,"resolve":0.6}
  
  -- Batch 처리 상태
  batch_request_id TEXT,
  batch_status TEXT DEFAULT 'pending',  -- pending, processing, completed, failed
  batch_response TEXT,                  -- Claude Batch API 전체 응답 (JSON)
  
  -- 개별 API 결과 URL
  suno_url TEXT,
  suno_audio_path TEXT,                 -- 로컬 저장 경로
  fish_url TEXT,
  fish_audio_path TEXT,
  hedra_url TEXT,
  hedra_video_path TEXT,
  runway_url TEXT,
  runway_video_path TEXT,
  
  -- 최종 영상
  final_video_path TEXT,                -- 30초 완성 영상 경로
  thumbnail_path TEXT,
  
  -- YouTube 정보
  youtube_url TEXT,
  youtube_video_id TEXT,
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
  status TEXT DEFAULT 'pending',        -- pending, processing, completed, failed
  processing_error TEXT,                -- 에러 메시지
  
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
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  character_name TEXT NOT NULL UNIQUE,
  
  -- Fish Audio 음성 ID
  fish_audio_voice_id TEXT,
  
  -- Hedra Identity Anchor
  identity_anchor_s3_path TEXT,
  identity_anchor_image_url TEXT,
  identity_anchor_local_path TEXT,      -- 로컬 저장 경로
  
  -- 기본 감정
  default_emotion TEXT,
  default_fear REAL DEFAULT 0.0,
  default_resolve REAL DEFAULT 0.5,
  default_confusion REAL DEFAULT 0.0,
  default_fatigue REAL DEFAULT 0.0,
  
  -- 메타데이터
  age_description TEXT,
  gender TEXT,
  description TEXT,                     -- 캐릭터 설명
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP
);

-- 테이블 3: api_usage_log (API 사용 로그)
CREATE TABLE IF NOT EXISTS api_usage_log (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  api_name TEXT NOT NULL,               -- claude, hedra, suno, fish_audio, runway
  scripture_id INTEGER,
  request_type TEXT,                    -- batch, generate, synthesis
  request_url TEXT,
  request_body TEXT,                    -- JSON
  response_status INTEGER,
  response_body TEXT,                   -- JSON
  duration_ms INTEGER,                  -- 응답 시간 (밀리초)
  cost_usd REAL DEFAULT 0.0,           -- 비용 (USD)
  error_message TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  
  FOREIGN KEY (scripture_id) REFERENCES scripture(id)
);

CREATE INDEX IF NOT EXISTS idx_api_name ON api_usage_log(api_name);
CREATE INDEX IF NOT EXISTS idx_api_created ON api_usage_log(created_at);

-- 테이블 4: youtube_analytics (YouTube 통계)
CREATE TABLE IF NOT EXISTS youtube_analytics (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  scripture_id INTEGER,
  date DATE NOT NULL,
  views INTEGER DEFAULT 0,
  watch_time_hours REAL DEFAULT 0.0,
  revenue REAL DEFAULT 0.0,
  likes INTEGER DEFAULT 0,
  comments INTEGER DEFAULT 0,
  shares INTEGER DEFAULT 0,
  subscribers_gained INTEGER DEFAULT 0,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  
  FOREIGN KEY (scripture_id) REFERENCES scripture(id),
  UNIQUE(scripture_id, date)
);

CREATE INDEX IF NOT EXISTS idx_youtube_date ON youtube_analytics(date);

-- 테이블 5: workflow_execution_log (워크플로우 실행 로그)
CREATE TABLE IF NOT EXISTS workflow_execution_log (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  workflow_name TEXT NOT NULL,         -- morning_batch, evening_generation, daily_monitoring
  execution_id TEXT,                    -- n8n execution ID
  status TEXT,                          -- success, failed, running
  start_time TIMESTAMP,
  end_time TIMESTAMP,
  duration_seconds INTEGER,
  error_message TEXT,
  metadata TEXT,                        -- JSON 형식
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_workflow_name ON workflow_execution_log(workflow_name);
CREATE INDEX IF NOT EXISTS idx_workflow_status ON workflow_execution_log(status);

-- 초기 캐릭터 데이터 삽입
INSERT OR IGNORE INTO character_voices (character_name, fish_audio_voice_id, identity_anchor_image_url, default_emotion, default_fear, default_resolve, age_description, gender, description) VALUES
  ('abraham', 'abraham_voice_id_1', 'https://example.com/characters/abraham.jpg', 'reverent_fear', 0.8, 0.9, '137세의 할아버지', 'male', '아브라함 - 믿음의 조상'),
  ('david', 'david_voice_id_1', 'https://example.com/characters/david.jpg', 'kingly_resolve', 0.3, 0.95, '젊은 왕', 'male', '다윗 - 이스라엘의 왕'),
  ('moses', 'moses_voice_id_1', 'https://example.com/characters/moses.jpg', 'prophetic_awe', 0.6, 0.9, '나이 든 선지자', 'male', '모세 - 율법을 받은 선지자'),
  ('eve', 'eve_voice_id_1', 'https://example.com/characters/eve.jpg', 'innocent_curiosity', 0.2, 0.5, '젊은 여성', 'female', '하와 - 최초의 여인'),
  ('jacob', 'jacob_voice_id_1', 'https://example.com/characters/jacob.jpg', 'struggling_resolve', 0.5, 0.7, '중년 남성', 'male', '야곱 - 이스라엘의 조상'),
  ('joseph', 'joseph_voice_id_1', 'https://example.com/characters/joseph.jpg', 'wise_forgiveness', 0.3, 0.9, '중년 남성', 'male', '요셉 - 꿈을 해석한 총리'),
  ('mary', 'mary_voice_id_1', 'https://example.com/characters/mary.jpg', 'humble_acceptance', 0.4, 0.95, '젊은 여성', 'female', '마리아 - 예수의 어머니'),
  ('jesus', 'jesus_voice_id_1', 'https://example.com/characters/jesus.jpg', 'compassionate_authority', 0.1, 1.0, '30대 남성', 'male', '예수 - 구세주'),
  ('peter', 'peter_voice_id_1', 'https://example.com/characters/peter.jpg', 'passionate_zeal', 0.4, 0.8, '중년 남성', 'male', '베드로 - 열두 제자 중 하나'),
  ('paul', 'paul_voice_id_1', 'https://example.com/characters/paul.jpg', 'fervent_conviction', 0.3, 0.95, '중년 남성', 'male', '바울 - 복음을 전한 사도');

-- 샘플 성경 구절 (나중에 seed_data.sql로 대체)
INSERT OR IGNORE INTO scripture (book_name, chapter, verse, korean_text, character_main, emotion_primary, fear_level, resolve_level) VALUES
  ('창세기', 22, 2, '하나님이 이르시되 네 아들 네 사랑하는 독자 이삭을 데리고 모리아 땅으로 가서 내가 네게 지시하는 한 산 거기서 그를 번제로 드리라 하시니라', 'abraham', 'fear', 0.9, 0.95),
  ('시편', 23, 1, '여호와는 나의 목자시니 내게 부족함이 없으리로다', 'david', 'hope', 0.1, 0.9),
  ('출애굽기', 3, 14, '하나님이 모세에게 이르시되 나는 스스로 있는 자니라 또 이르시되 너는 이스라엘 자손에게 이같이 이르기를 스스로 있는 자가 나를 너희에게 보내셨다 하라 하시니라', 'moses', 'awe', 0.7, 0.9);
