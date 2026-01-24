-- 빠른 데이터베이스 초기화 (Railway 터미널에서 직접 실행)

-- 테이블 생성
CREATE TABLE IF NOT EXISTS scripture (
  id SERIAL PRIMARY KEY,
  book_name VARCHAR(255) NOT NULL,
  chapter INTEGER NOT NULL,
  verse INTEGER NOT NULL,
  korean_text TEXT NOT NULL,
  character_main VARCHAR(100),
  character_secondary VARCHAR(100),
  emotion_primary VARCHAR(50),
  emotion_secondary VARCHAR(50),
  fear_level REAL DEFAULT 0.0,
  resolve_level REAL DEFAULT 0.0,
  confusion_level REAL DEFAULT 0.0,
  fatigue_level REAL DEFAULT 0.0,
  grief_level REAL DEFAULT 0.0,
  hope_level REAL DEFAULT 0.0,
  visual_prompt TEXT,
  vocal_prompt TEXT,
  music_prompt TEXT,
  emotion_values TEXT,
  batch_request_id VARCHAR(255),
  batch_status VARCHAR(50) DEFAULT 'pending',
  batch_response TEXT,
  suno_url TEXT,
  suno_audio_path TEXT,
  fish_url TEXT,
  fish_audio_path TEXT,
  hedra_url TEXT,
  hedra_video_path TEXT,
  runway_url TEXT,
  runway_video_path TEXT,
  final_video_path TEXT,
  thumbnail_path TEXT,
  youtube_url TEXT,
  youtube_video_id VARCHAR(255),
  youtube_views INTEGER DEFAULT 0,
  youtube_watch_time_hours REAL DEFAULT 0.0,
  youtube_revenue REAL DEFAULT 0.0,
  youtube_likes INTEGER DEFAULT 0,
  youtube_comments INTEGER DEFAULT 0,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  batch_request_date TIMESTAMP,
  generation_date TIMESTAMP,
  upload_date TIMESTAMP,
  status VARCHAR(50) DEFAULT 'pending',
  processing_error TEXT,
  notes TEXT
);

CREATE INDEX IF NOT EXISTS idx_status ON scripture(status);
CREATE INDEX IF NOT EXISTS idx_batch_status ON scripture(batch_status);
CREATE INDEX IF NOT EXISTS idx_character ON scripture(character_main);
CREATE INDEX IF NOT EXISTS idx_emotion ON scripture(emotion_primary);
CREATE INDEX IF NOT EXISTS idx_book_chapter_verse ON scripture(book_name, chapter, verse);

CREATE TABLE IF NOT EXISTS character_voices (
  id SERIAL PRIMARY KEY,
  character_name VARCHAR(100) NOT NULL UNIQUE,
  fish_audio_voice_id VARCHAR(255),
  identity_anchor_s3_path TEXT,
  identity_anchor_image_url TEXT,
  identity_anchor_local_path TEXT,
  default_emotion VARCHAR(50),
  default_fear REAL DEFAULT 0.0,
  default_resolve REAL DEFAULT 0.5,
  default_confusion REAL DEFAULT 0.0,
  default_fatigue REAL DEFAULT 0.0,
  age_description VARCHAR(255),
  gender VARCHAR(20),
  description TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP
);

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

-- 샘플 데이터
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

INSERT INTO scripture (book_name, chapter, verse, korean_text, character_main, emotion_primary, fear_level, resolve_level, confusion_level) VALUES
  ('창세기', 1, 1, '태초에 하나님이 천지를 창조하시니라', NULL, 'awe', 0.0, 0.0, 0.0),
  ('창세기', 3, 6, '여자가 그 나무를 본즉 먹음직도 하고 보암직도 하고 지혜롭게 할 만큼 탐스럽기도 한 나무인지라 여자가 그 열매를 따먹고 자기와 함께 있는 남편에게도 주매 그도 먹은지라', 'eve', 'curiosity', 0.2, 0.3, 0.5),
  ('창세기', 12, 1, '여호와께서 아브람에게 이르시되 너는 너의 고향과 친척과 아버지의 집을 떠나 내가 네게 보여 줄 땅으로 가라', 'abraham', 'resolve', 0.4, 0.9, 0.3),
  ('창세기', 22, 1, '그 일 후에 하나님이 아브라함을 시험하시려고 그를 부르시되 아브라함아 하시니 그가 이르되 내가 여기 있나이다 하시니라', 'abraham', 'fear', 0.7, 0.8, 0.2),
  ('창세기', 22, 2, '하나님이 이르시되 네 아들 네 사랑하는 독자 이삭을 데리고 모리아 땅으로 가서 내가 네게 지시하는 한 산 거기서 그를 번제로 드리라 하시니라', 'abraham', 'fear', 0.9, 0.95, 0.1),
  ('창세기', 32, 24, '야곱이 홀로 남았더니 어떤 사람이 날이 새도록 야곱과 씨름하다가', 'jacob', 'struggle', 0.6, 0.8, 0.4),
  ('창세기', 37, 5, '요셉이 꿈을 꾸고 자기 형들에게 말하매 그들이 그를 더욱 미워하더라', 'joseph', 'innocence', 0.2, 0.5, 0.3),
  ('출애굽기', 3, 2, '여호와의 사자가 떨기나무 가운데로부터 그에게 나타나시니라 보라 떨기나무에 불이 타는데 떨기나무는 사라지지 아니하더라', 'moses', 'awe', 0.8, 0.7, 0.5),
  ('출애굽기', 3, 14, '하나님이 모세에게 이르시되 나는 스스로 있는 자니라 또 이르시되 너는 이스라엘 자손에게 이같이 이르기를 스스로 있는 자가 나를 너희에게 보내셨다 하라 하시니라', 'moses', 'awe', 0.7, 0.9, 0.2),
  ('출애굽기', 14, 21, '모세가 바다를 향하여 손을 내밀매 여호와께서 큰 바람으로 밤새도록 바닷물을 물러가게 하시니 물이 갈라져 바다가 마른 땅이 된지라', 'moses', 'awe', 0.3, 1.0, 0.0),
  ('시편', 23, 1, '여호와는 나의 목자시니 내게 부족함이 없으리로다', 'david', 'hope', 0.1, 0.9, 0.0),
  ('시편', 23, 4, '내가 사망의 음침한 골짜기로 다닐지라도 해를 두려워하지 않을 것은 주께서 나와 함께 하심이라 주의 지팡이와 막대기가 나를 안위하시나이다', 'david', 'hope', 0.3, 0.95, 0.0),
  ('시편', 51, 1, '하나님이여 주의 인자하심을 따라 나를 긍휼히 여기시며 주의 많은 자비를 따라 내 죄과를 도말하소서', 'david', 'sorrow', 0.5, 0.7, 0.0),
  ('누가복음', 1, 38, '마리아가 이르되 주의 여종이오니 말씀대로 내게 이루어지이다 하매 천사가 떠나가니라', 'mary', 'acceptance', 0.4, 0.95, 0.0),
  ('마태복음', 5, 3, '심령이 가난한 자는 복이 있나니 천국이 그들의 것임이요', 'jesus', 'compassion', 0.0, 1.0, 0.0),
  ('마태복음', 6, 9, '그러므로 너희는 이렇게 기도하라 하늘에 계신 우리 아버지여 이름이 거룩히 여김을 받으시오며', 'jesus', 'reverence', 0.0, 1.0, 0.0),
  ('마태복음', 26, 39, '조금 나아가사 얼굴을 땅에 대시고 엎드려 기도하여 이르시되 내 아버지여 만일 할 만하시거든 이 잔을 내게서 지나가게 하옵소서 그러나 나의 원대로 하지 마시고 아버지의 원대로 하옵소서 하시고', 'jesus', 'sorrow', 0.6, 1.0, 0.0),
  ('마태복음', 16, 18, '또 내가 네게 이르노니 너는 베드로라 내가 이 반석 위에 내 교회를 세우리니 음부의 권세가 이기지 못하리라', 'peter', 'awe', 0.5, 0.9, 0.0),
  ('사도행전', 9, 4, '땅에 엎드러져 들으매 소리가 있어 이르시되 사울아 사울아 네가 어찌하여 나를 박해하느냐 하시거늘', 'paul', 'awe', 0.9, 0.8, 0.0),
  ('고린도전서', 13, 4, '사랑은 오래 참고 사랑은 온유하며 시기하지 아니하며 사랑은 자랑하지 아니하며 교만하지 아니하며', 'paul', 'compassion', 0.0, 0.9, 0.0)
ON CONFLICT DO NOTHING;

UPDATE scripture SET status = 'pending' WHERE status IS NULL;

SELECT '데이터베이스 초기화 완료!' as message;
SELECT COUNT(*) as total_scriptures FROM scripture;
SELECT COUNT(*) as total_characters FROM character_voices;
