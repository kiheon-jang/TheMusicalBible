-- The Musical Bible - 테스트용 더미 데이터
-- 파이프라인 테스트를 위한 성경 구절 샘플

-- 기존 데이터 삭제 (테스트용)
-- DELETE FROM scripture WHERE id > 0;

-- 테스트 구절 1: 창세기 22:1-2 (아브라함의 번제, 노년)
INSERT INTO scripture (
  book_name, chapter, verse, korean_text,
  character_main, character_secondary,
  emotion_primary, emotion_secondary,
  fear_level, resolve_level, confusion_level, fatigue_level, hope_level,
  status, batch_status
) VALUES (
  '창세기', 22, 1,
  '이 일 후에 하나님이 아브라함을 시험하시려고 그를 부르시되 아브라함아 하시니 그가 이르되 내가 여기 있나이다',
  'abraham', NULL,
  'fearful_obedience', 'determination',
  0.8, 0.9, 0.5, 0.3, 0.7,
  'pending', 'pending'
);

-- 테스트 구절 2: 창세기 22:2 (이삭을 번제로 드리라는 명령, 아브라함 노년)
INSERT INTO scripture (
  book_name, chapter, verse, korean_text,
  character_main, character_secondary,
  emotion_primary, emotion_secondary,
  fear_level, resolve_level, confusion_level, fatigue_level, hope_level,
  status, batch_status
) VALUES (
  '창세기', 22, 2,
  '여호와께서 이르시되 네 아들 네 사랑하는 독자 이삭을 데리고 모리아 땅으로 가서 내가 네게 일러 준 한 산 거기서 그를 번제로 드리라',
  'abraham', 'isaac',
  'anguished_faith', 'obedience',
  0.9, 0.95, 0.8, 0.4, 0.6,
  'pending', 'pending'
);

-- 테스트 구절 3: 사무엘상 17:45 (다윗과 골리앗, 다윗 청년)
INSERT INTO scripture (
  book_name, chapter, verse, korean_text,
  character_main, character_secondary,
  emotion_primary, emotion_secondary,
  fear_level, resolve_level, confusion_level, fatigue_level, hope_level,
  status, batch_status
) VALUES (
  '사무엘상', 17, 45,
  '다윗이 블레셋 사람에게 이르되 너는 칼과 창과 단창으로 내게 나아오거니와 나는 만군의 여호와의 이름 곧 네가 모욕하는 이스라엘 군대의 하나님의 이름으로 네게 나아가노라',
  'david', 'goliath',
  'fearless_faith', 'confidence',
  0.2, 0.95, 0.1, 0.0, 0.9,
  'pending', 'pending'
);

-- 테스트 구절 4: 출애굽기 3:4 (불타는 떨기나무, 모세 노년)
INSERT INTO scripture (
  book_name, chapter, verse, korean_text,
  character_main, character_secondary,
  emotion_primary, emotion_secondary,
  fear_level, resolve_level, confusion_level, fatigue_level, hope_level,
  status, batch_status
) VALUES (
  '출애굽기', 3, 4,
  '여호와께서 그가 보려고 돌이켜 오는 것을 보신지라 하나님이 떨기나무 가운데서 그를 불러 이르시되 모세야 모세야 하시매 그가 이르되 내가 여기 있나이다',
  'moses', NULL,
  'awe', 'fear',
  0.7, 0.4, 0.6, 0.3, 0.5,
  'pending', 'pending'
);

-- 테스트 구절 5: 창세기 28:16 (야곱의 사다리, 야곱 청년)
INSERT INTO scripture (
  book_name, chapter, verse, korean_text,
  character_main, character_secondary,
  emotion_primary, emotion_secondary,
  fear_level, resolve_level, confusion_level, fatigue_level, hope_level,
  status, batch_status
) VALUES (
  '창세기', 28, 16,
  '야곱이 잠에서 깨어 이르되 여호와께서 과연 여기 계시거늘 내가 알지 못하였도다',
  'jacob', NULL,
  'shocked_realization', 'awe',
  0.6, 0.5, 0.7, 0.4, 0.8,
  'pending', 'pending'
);

-- 검증 쿼리
SELECT 
  id,
  book_name,
  chapter,
  verse,
  character_main,
  emotion_primary,
  fear_level,
  resolve_level,
  status,
  batch_status
FROM scripture
WHERE status = 'pending'
ORDER BY id DESC
LIMIT 5;

-- 완료 메시지
SELECT '테스트 데이터 5개 삽입 완료! 파이프라인을 실행하세요.' AS status;
