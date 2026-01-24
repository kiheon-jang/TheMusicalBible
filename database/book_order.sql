-- The Musical Bible (TMB) - 성경 66권 순서 정의
-- 순차적 처리를 위한 책 순서 관리

CREATE TABLE IF NOT EXISTS book_order (
  id SERIAL PRIMARY KEY,
  book_number INTEGER NOT NULL UNIQUE,
  book_name_korean VARCHAR(50) NOT NULL UNIQUE,
  book_name_english VARCHAR(50) NOT NULL,
  testament VARCHAR(10) NOT NULL CHECK (testament IN ('OLD', 'NEW')),
  chapter_count INTEGER NOT NULL,
  verse_count INTEGER NOT NULL
);

-- 구약 39권
INSERT INTO book_order (book_number, book_name_korean, book_name_english, testament, chapter_count, verse_count) VALUES
  (1, '창세기', 'Genesis', 'OLD', 50, 1533),
  (2, '출애굽기', 'Exodus', 'OLD', 40, 1213),
  (3, '레위기', 'Leviticus', 'OLD', 27, 859),
  (4, '민수기', 'Numbers', 'OLD', 36, 1288),
  (5, '신명기', 'Deuteronomy', 'OLD', 34, 959),
  (6, '여호수아', 'Joshua', 'OLD', 24, 658),
  (7, '사사기', 'Judges', 'OLD', 21, 618),
  (8, '룻기', 'Ruth', 'OLD', 4, 85),
  (9, '사무엘상', '1 Samuel', 'OLD', 31, 810),
  (10, '사무엘하', '2 Samuel', 'OLD', 24, 695),
  (11, '열왕기상', '1 Kings', 'OLD', 22, 816),
  (12, '열왕기하', '2 Kings', 'OLD', 25, 719),
  (13, '역대상', '1 Chronicles', 'OLD', 29, 942),
  (14, '역대하', '2 Chronicles', 'OLD', 36, 822),
  (15, '에스라', 'Ezra', 'OLD', 10, 280),
  (16, '느헤미야', 'Nehemiah', 'OLD', 13, 406),
  (17, '에스더', 'Esther', 'OLD', 10, 167),
  (18, '욥기', 'Job', 'OLD', 42, 1070),
  (19, '시편', 'Psalms', 'OLD', 150, 2461),
  (20, '잠언', 'Proverbs', 'OLD', 31, 915),
  (21, '전도서', 'Ecclesiastes', 'OLD', 12, 222),
  (22, '아가', 'Song of Solomon', 'OLD', 8, 117),
  (23, '이사야', 'Isaiah', 'OLD', 66, 1292),
  (24, '예레미야', 'Jeremiah', 'OLD', 52, 1364),
  (25, '예레미야애가', 'Lamentations', 'OLD', 5, 154),
  (26, '에스겔', 'Ezekiel', 'OLD', 48, 1273),
  (27, '다니엘', 'Daniel', 'OLD', 12, 357),
  (28, '호세아', 'Hosea', 'OLD', 14, 197),
  (29, '요엘', 'Joel', 'OLD', 3, 73),
  (30, '아모스', 'Amos', 'OLD', 9, 146),
  (31, '오바댜', 'Obadiah', 'OLD', 1, 21),
  (32, '요나', 'Jonah', 'OLD', 4, 48),
  (33, '미가', 'Micah', 'OLD', 7, 105),
  (34, '나훔', 'Nahum', 'OLD', 3, 47),
  (35, '하박국', 'Habakkuk', 'OLD', 3, 56),
  (36, '스바냐', 'Zephaniah', 'OLD', 3, 53),
  (37, '학개', 'Haggai', 'OLD', 2, 38),
  (38, '스가랴', 'Zechariah', 'OLD', 14, 211),
  (39, '말라기', 'Malachi', 'OLD', 4, 55),
  
  -- 신약 27권
  (40, '마태복음', 'Matthew', 'NEW', 28, 1071),
  (41, '마가복음', 'Mark', 'NEW', 16, 678),
  (42, '누가복음', 'Luke', 'NEW', 24, 1151),
  (43, '요한복음', 'John', 'NEW', 21, 879),
  (44, '사도행전', 'Acts', 'NEW', 28, 1007),
  (45, '로마서', 'Romans', 'NEW', 16, 433),
  (46, '고린도전서', '1 Corinthians', 'NEW', 16, 437),
  (47, '고린도후서', '2 Corinthians', 'NEW', 13, 257),
  (48, '갈라디아서', 'Galatians', 'NEW', 6, 149),
  (49, '에베소서', 'Ephesians', 'NEW', 6, 155),
  (50, '빌립보서', 'Philippians', 'NEW', 4, 104),
  (51, '골로새서', 'Colossians', 'NEW', 4, 95),
  (52, '데살로니가전서', '1 Thessalonians', 'NEW', 5, 89),
  (53, '데살로니가후서', '2 Thessalonians', 'NEW', 3, 47),
  (54, '디모데전서', '1 Timothy', 'NEW', 6, 113),
  (55, '디모데후서', '2 Timothy', 'NEW', 4, 83),
  (56, '디도서', 'Titus', 'NEW', 3, 46),
  (57, '빌레몬서', 'Philemon', 'NEW', 1, 25),
  (58, '히브리서', 'Hebrews', 'NEW', 13, 303),
  (59, '야고보서', 'James', 'NEW', 5, 108),
  (60, '베드로전서', '1 Peter', 'NEW', 5, 105),
  (61, '베드로후서', '2 Peter', 'NEW', 3, 61),
  (62, '요한일서', '1 John', 'NEW', 5, 105),
  (63, '요한이서', '2 John', 'NEW', 1, 13),
  (64, '요한삼서', '3 John', 'NEW', 1, 14),
  (65, '유다서', 'Jude', 'NEW', 1, 25),
  (66, '요한계시록', 'Revelation', 'NEW', 22, 404)
ON CONFLICT (book_number) DO NOTHING;

-- 인덱스 추가
CREATE INDEX IF NOT EXISTS idx_book_number ON book_order(book_number);
CREATE INDEX IF NOT EXISTS idx_book_name ON book_order(book_name_korean);

-- 통계 출력
SELECT 
  testament, 
  COUNT(*) as book_count,
  SUM(chapter_count) as total_chapters,
  SUM(verse_count) as total_verses
FROM book_order
GROUP BY testament
ORDER BY testament;

SELECT '✅ 책 순서 테이블 생성 완료!' as status;
