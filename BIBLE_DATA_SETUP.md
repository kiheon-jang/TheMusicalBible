---
date: 2026-01-26
project: 10_Projects/project
tags: ['project']
---
# 📖 성경 데이터 셋업 가이드

## 🎯 목표
한글 개역개정 성경 전체(31,102개 구절)를 PostgreSQL에 순차적으로 입력

---

## 📊 성경 데이터 소스

### Option 1: GitHub - boring-km/nkrv_bible ✅ 추천
```
Repository: https://github.com/boring-km/nkrv_bible
Format: JSON
Translation: 개역개정 (New Korean Revised Version)
Status: ✅ 무료 공개
```

### Option 2: GitHub - aromkimm/bible
```
Repository: https://github.com/aromkimm/bible
Format: JSON
Translation: 개역개정
Status: ✅ 무료 공개
```

### Option 3: Bible API
```
API: https://bibleapi.co/
Format: REST API
Translations: 여러 버전 지원
Status: ⚠️ API 키 필요
```

---

## ⚠️ 저작권 주의사항

**대한성서공회 저작권**:
- 개역개정 성경은 대한성서공회 저작권
- 비상업적 이용: 허가 필요 (하지만 일반적으로 교육/선교 목적은 허용)
- **The Musical Bible**: 비상업적 선교/교육 콘텐츠로 분류 가능
- YouTube 광고 수익 발생 시 저작권 확인 필요

**권장사항**:
1. 대한성서공회에 공식 문의 (copyright@bskorea.or.kr)
2. 프로젝트 설명 및 비상업적 목적 명시
3. 성경 출처 명시: "개역개정 성경 ⓒ 대한성서공회"

---

## 🔧 구현 방법

### Step 1: 책 순서 테이블 생성

**파일**: `database/book_order.sql`

```sql
-- 성경 66권 순서 정의
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
  (39, '말라기', 'Malachi', 'OLD', 4, 55);

-- 신약 27권
INSERT INTO book_order (book_number, book_name_korean, book_name_english, testament, chapter_count, verse_count) VALUES
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
  (66, '요한계시록', 'Revelation', 'NEW', 22, 404);

-- 인덱스 추가
CREATE INDEX IF NOT EXISTS idx_book_number ON book_order(book_number);
CREATE INDEX IF NOT EXISTS idx_book_name ON book_order(book_name_korean);
```

---

### Step 2: 성경 데이터 수집 스크립트

**파일**: `scripts/fetch_bible_data.py`

```python
#!/usr/bin/env python3
"""
The Musical Bible (TMB) - 성경 데이터 수집 스크립트
GitHub에서 개역개정 성경 JSON 데이터를 가져와 PostgreSQL에 저장
"""

import json
import requests
import psycopg2
from psycopg2.extras import execute_batch
import os
from typing import List, Dict

# GitHub 저장소 URL (raw JSON)
BIBLE_DATA_URLS = {
    "boring-km/nkrv_bible": "https://raw.githubusercontent.com/boring-km/nkrv_bible/main/bible.json",
    "aromkimm/bible": "https://raw.githubusercontent.com/aromkimm/bible/master/bible.json"
}

# PostgreSQL 연결 정보
DATABASE_URL = os.getenv("DATABASE_URL") or "postgresql://user:password@localhost:5432/tmb"

class BibleDataFetcher:
    def __init__(self, db_url: str):
        self.db_url = db_url
        self.conn = None
        self.cursor = None
    
    def connect_db(self):
        """PostgreSQL 연결"""
        try:
            self.conn = psycopg2.connect(self.db_url)
            self.cursor = self.conn.cursor()
            print("✅ PostgreSQL 연결 성공")
        except Exception as e:
            print(f"❌ DB 연결 실패: {e}")
            raise
    
    def fetch_from_github(self, source: str = "boring-km/nkrv_bible") -> Dict:
        """GitHub에서 성경 데이터 가져오기"""
        url = BIBLE_DATA_URLS.get(source)
        if not url:
            raise ValueError(f"Unknown source: {source}")
        
        print(f"📥 데이터 다운로드 중: {source}")
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        
        data = response.json()
        print(f"✅ 데이터 다운로드 완료: {len(data)} 권")
        return data
    
    def parse_bible_data(self, raw_data: Dict) -> List[Dict]:
        """
        JSON 데이터를 scripture 테이블 형식으로 변환
        
        예상 구조:
        {
          "창세기": {
            "1": {
              "1": "태초에 하나님이 천지를 창조하시니라",
              "2": "땅이 혼돈하고 공허하며..."
            }
          }
        }
        """
        scriptures = []
        
        for book_name, chapters in raw_data.items():
            for chapter_num, verses in chapters.items():
                for verse_num, text in verses.items():
                    scriptures.append({
                        "book_name": book_name,
                        "chapter": int(chapter_num),
                        "verse": int(verse_num),
                        "korean_text": text,
                        "status": "pending"  # 초기 상태
                    })
        
        print(f"✅ 총 {len(scriptures)}개 구절 파싱 완료")
        return scriptures
    
    def insert_to_db(self, scriptures: List[Dict]):
        """PostgreSQL에 데이터 삽입"""
        query = """
        INSERT INTO scripture 
          (book_name, chapter, verse, korean_text, status)
        VALUES 
          (%(book_name)s, %(chapter)s, %(verse)s, %(korean_text)s, %(status)s)
        ON CONFLICT (book_name, chapter, verse) DO NOTHING
        """
        
        try:
            execute_batch(self.cursor, query, scriptures, page_size=1000)
            self.conn.commit()
            print(f"✅ {len(scriptures)}개 구절 DB 저장 완료")
        except Exception as e:
            self.conn.rollback()
            print(f"❌ DB 저장 실패: {e}")
            raise
    
    def add_unique_constraint(self):
        """book_name, chapter, verse 조합에 유니크 제약 추가"""
        try:
            self.cursor.execute("""
                ALTER TABLE scripture 
                ADD CONSTRAINT unique_scripture 
                UNIQUE (book_name, chapter, verse)
            """)
            self.conn.commit()
            print("✅ 유니크 제약 추가 완료")
        except psycopg2.errors.DuplicateTable:
            self.conn.rollback()
            print("⚠️  유니크 제약 이미 존재")
        except Exception as e:
            self.conn.rollback()
            print(f"⚠️  유니크 제약 추가 실패: {e}")
    
    def verify_data(self):
        """데이터 검증"""
        self.cursor.execute("SELECT COUNT(*) FROM scripture")
        count = self.cursor.fetchone()[0]
        print(f"📊 총 구절 수: {count}")
        
        self.cursor.execute("""
            SELECT book_name, COUNT(*) 
            FROM scripture 
            GROUP BY book_name 
            ORDER BY MIN(id)
            LIMIT 10
        """)
        sample = self.cursor.fetchall()
        print("\n📖 책별 구절 수 (상위 10개):")
        for book, verse_count in sample:
            print(f"  - {book}: {verse_count}개")
    
    def close(self):
        """연결 종료"""
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
        print("✅ DB 연결 종료")


def main():
    """메인 실행 함수"""
    print("=" * 50)
    print("📖 The Musical Bible - 성경 데이터 수집 시작")
    print("=" * 50)
    
    fetcher = BibleDataFetcher(DATABASE_URL)
    
    try:
        # 1. DB 연결
        fetcher.connect_db()
        
        # 2. 유니크 제약 추가 (중복 방지)
        fetcher.add_unique_constraint()
        
        # 3. GitHub에서 데이터 가져오기
        raw_data = fetcher.fetch_from_github("boring-km/nkrv_bible")
        
        # 4. 데이터 파싱
        scriptures = fetcher.parse_bible_data(raw_data)
        
        # 5. DB에 저장
        fetcher.insert_to_db(scriptures)
        
        # 6. 검증
        fetcher.verify_data()
        
        print("\n" + "=" * 50)
        print("🎉 성경 데이터 수집 완료!")
        print("=" * 50)
        
    except Exception as e:
        print(f"\n❌ 에러 발생: {e}")
        raise
    finally:
        fetcher.close()


if __name__ == "__main__":
    main()
```

**의존성**:
```bash
pip install psycopg2-binary requests
```

---

### Step 3: 캐릭터 자동 매핑 (Optional)

**파일**: `scripts/assign_characters.py`

```python
#!/usr/bin/env python3
"""
주요 캐릭터를 성경 구절에 자동 할당
"""

import psycopg2
import os

DATABASE_URL = os.getenv("DATABASE_URL")

# 캐릭터 매핑 규칙
CHARACTER_MAPPING = {
    "아브람": "abraham",
    "아브라함": "abraham",
    "사라": "sarah",
    "이삭": "isaac",
    "야곱": "jacob",
    "요셉": "joseph",
    "모세": "moses",
    "다윗": "david",
    "솔로몬": "solomon",
    "엘리야": "elijah",
    "엘리사": "elisha",
    "이사야": "isaiah",
    "예레미야": "jeremiah",
    "에스겔": "ezekiel",
    "다니엘": "daniel",
    "예수": "jesus",
    "마리아": "mary",
    "베드로": "peter",
    "바울": "paul",
    "요한": "john"
}

def assign_characters(db_url):
    conn = psycopg2.connect(db_url)
    cursor = conn.cursor()
    
    for korean_name, english_name in CHARACTER_MAPPING.items():
        query = """
        UPDATE scripture 
        SET character_main = %s
        WHERE korean_text LIKE %s
          AND character_main IS NULL
        """
        cursor.execute(query, (english_name, f"%{korean_name}%"))
        updated = cursor.rowcount
        print(f"✅ {korean_name} ({english_name}): {updated}개 구절 업데이트")
    
    conn.commit()
    cursor.close()
    conn.close()
    
    print("\n🎭 캐릭터 할당 완료!")

if __name__ == "__main__":
    assign_characters(DATABASE_URL)
```

---

## 🚀 실행 방법

### 1. 책 순서 테이블 생성
```bash
psql $DATABASE_URL < database/book_order.sql
```

### 2. 성경 데이터 수집
```bash
export DATABASE_URL="postgresql://user:password@railway.app:5432/railway"
python3 scripts/fetch_bible_data.py
```

### 3. 캐릭터 자동 할당 (선택)
```bash
python3 scripts/assign_characters.py
```

### 4. 순차 처리 확인
```sql
-- 순서대로 pending 구절 3개 조회
SELECT s.id, b.book_number, s.book_name, s.chapter, s.verse, s.korean_text
FROM scripture s
JOIN book_order b ON s.book_name = b.book_name_korean
WHERE s.status = 'pending'
ORDER BY b.book_number, s.chapter, s.verse
LIMIT 3;
```

---

## 📊 워크플로우 수정

**파일**: `workflows/complete_pipeline.json`

**"구절 3개 조회" 노드 수정**:
```json
{
  "id": "postgres-fetch-scripture",
  "name": "PostgreSQL: 구절 3개 조회",
  "parameters": {
    "operation": "executeQuery",
    "query": "SELECT s.id, s.book_name, s.chapter, s.verse, s.korean_text, s.character_main, s.emotion_primary, s.fear_level, s.resolve_level, s.confusion_level FROM scripture s JOIN book_order b ON s.book_name = b.book_name_korean WHERE s.status = 'pending' ORDER BY b.book_number, s.chapter, s.verse LIMIT 3"
  }
}
```

**핵심 변경**:
- `JOIN book_order` 추가
- `ORDER BY b.book_number, s.chapter, s.verse` → 순차적 처리

---

## ✅ 완료 조건

- [ ] `book_order` 테이블 생성 (66권)
- [ ] `fetch_bible_data.py` 실행 (31,102개 구절)
- [ ] `assign_characters.py` 실행 (주요 캐릭터)
- [ ] `complete_pipeline.json` 쿼리 수정
- [ ] 순차 처리 확인 (창세기 1:1부터)

---

## 🎯 결과

```
✅ 창세기 1:1 → ... → 요한계시록 22:21 순차 처리
✅ 매일 3개씩 자동 생성
✅ 약 10,367일 (28.4년) 완성 예정

(빠른 처리를 위해 LIMIT 3 → 10으로 변경 가능)
```

---

## 📞 대한성서공회 문의 템플릿

```
제목: 개역개정 성경 비상업적 이용 문의

안녕하세요,

저는 The Musical Bible 프로젝트를 진행 중인 [이름]입니다.

[프로젝트 설명]
- 목적: 성경을 AI 기술로 뮤지컬 영상화하여 젊은 세대에게 전달
- 형식: YouTube 30초 숏츠 (무료 배포)
- 기술: AI 음성, 음악, 영상 합성
- 상업성: 비상업적 선교/교육 목적 (광고 수익 미정)

개역개정 성경 전체를 사용하고자 하는데, 
저작권 허가 절차와 조건에 대해 안내 부탁드립니다.

감사합니다.

연락처: [이메일/전화번호]
```

**대한성서공회 연락처**:
- 이메일: copyright@bskorea.or.kr
- 전화: 02-2001-0000
- 웹사이트: https://www.bskorea.or.kr

---

## 🎉 최종 확인

**성경 전체 데이터**: ✅ GitHub에서 수집  
**순차적 처리**: ✅ book_order 테이블로 관리  
**저작권**: ⚠️ 대한성서공회 문의 권장  
**자동화**: ✅ Python 스크립트 완성  

**이제 성경 전체를 순서대로 생성할 수 있습니다!** 🚀
