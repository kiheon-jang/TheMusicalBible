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
# Option 1: boring-km/nkrv_bible (개역개정)
# Option 2: 직접 다운로드하여 로컬 파일로 사용
BIBLE_DATA_URL = os.getenv("BIBLE_DATA_URL") or "https://raw.githubusercontent.com/boring-km/nkrv_bible/main/bible.json"

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
    
    def fetch_from_github(self, url: str = BIBLE_DATA_URL) -> Dict:
        """GitHub에서 성경 데이터 가져오기"""
        print(f"📥 데이터 다운로드 중: {url}")
        
        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            data = response.json()
            print(f"✅ 데이터 다운로드 완료: {len(data)} 권")
            return data
        except Exception as e:
            print(f"❌ 다운로드 실패: {e}")
            print("⚠️  대안: 로컬 파일을 사용하거나 다른 소스를 시도하세요")
            raise
    
    def load_from_file(self, filepath: str) -> Dict:
        """로컬 JSON 파일에서 데이터 로드"""
        print(f"📂 파일 로드 중: {filepath}")
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        print(f"✅ 파일 로드 완료: {len(data)} 권")
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
            if not isinstance(chapters, dict):
                continue
            
            for chapter_num, verses in chapters.items():
                if not isinstance(verses, dict):
                    continue
                
                for verse_num, text in verses.items():
                    if isinstance(text, str) and text.strip():
                        scriptures.append({
                            "book_name": book_name,
                            "chapter": int(chapter_num),
                            "verse": int(verse_num),
                            "korean_text": text.strip(),
                            "status": "pending"  # 초기 상태
                        })
        
        print(f"✅ 총 {len(scriptures)}개 구절 파싱 완료")
        return scriptures
    
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
        except psycopg2.errors.DuplicateObject:
            self.conn.rollback()
            print("⚠️  유니크 제약 이미 존재")
        except Exception as e:
            self.conn.rollback()
            print(f"⚠️  유니크 제약 추가 실패 (무시): {e}")
    
    def insert_to_db(self, scriptures: List[Dict], batch_size: int = 1000):
        """PostgreSQL에 데이터 삽입"""
        query = """
        INSERT INTO scripture 
          (book_name, chapter, verse, korean_text, status)
        VALUES 
          (%(book_name)s, %(chapter)s, %(verse)s, %(korean_text)s, %(status)s)
        ON CONFLICT (book_name, chapter, verse) DO NOTHING
        """
        
        try:
            print(f"📝 DB에 저장 중... (Batch size: {batch_size})")
            execute_batch(self.cursor, query, scriptures, page_size=batch_size)
            self.conn.commit()
            
            # 실제 삽입된 개수 확인
            self.cursor.execute("SELECT COUNT(*) FROM scripture")
            total = self.cursor.fetchone()[0]
            
            print(f"✅ DB 저장 완료! 총 {total}개 구절")
        except Exception as e:
            self.conn.rollback()
            print(f"❌ DB 저장 실패: {e}")
            raise
    
    def verify_data(self):
        """데이터 검증"""
        # 총 구절 수
        self.cursor.execute("SELECT COUNT(*) FROM scripture")
        count = self.cursor.fetchone()[0]
        print(f"\n📊 총 구절 수: {count:,}")
        
        # pending 상태 구절 수
        self.cursor.execute("SELECT COUNT(*) FROM scripture WHERE status = 'pending'")
        pending = self.cursor.fetchone()[0]
        print(f"⏳ 처리 대기 구절: {pending:,}")
        
        # 책별 구절 수 (상위 10개)
        self.cursor.execute("""
            SELECT book_name, COUNT(*) as verse_count
            FROM scripture 
            GROUP BY book_name 
            ORDER BY MIN(id)
            LIMIT 10
        """)
        sample = self.cursor.fetchall()
        print("\n📖 책별 구절 수 (상위 10개):")
        for book, verse_count in sample:
            print(f"  - {book}: {verse_count:,}개")
        
        # 순차 조회 테스트
        self.cursor.execute("""
            SELECT s.book_name, s.chapter, s.verse, 
                   SUBSTRING(s.korean_text, 1, 50) as preview
            FROM scripture s
            JOIN book_order b ON s.book_name = b.book_name_korean
            WHERE s.status = 'pending'
            ORDER BY b.book_number, s.chapter, s.verse
            LIMIT 5
        """)
        next_verses = self.cursor.fetchall()
        print("\n🎬 다음 처리 예정 구절 (순서대로):")
        for book, ch, v, preview in next_verses:
            print(f"  {book} {ch}:{v} - {preview}...")
    
    def close(self):
        """연결 종료"""
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
        print("\n✅ DB 연결 종료")


def main():
    """메인 실행 함수"""
    print("=" * 60)
    print("📖 The Musical Bible - 성경 데이터 수집 시작")
    print("=" * 60)
    
    fetcher = BibleDataFetcher(DATABASE_URL)
    
    try:
        # 1. DB 연결
        fetcher.connect_db()
        
        # 2. 유니크 제약 추가 (중복 방지)
        fetcher.add_unique_constraint()
        
        # 3. 데이터 가져오기
        # Option 1: GitHub에서 가져오기 (기본)
        try:
            raw_data = fetcher.fetch_from_github()
        except:
            # Option 2: 로컬 파일 사용
            print("\n⚠️  GitHub 다운로드 실패. 로컬 파일을 사용하세요:")
            print("   python3 scripts/fetch_bible_data.py --file bible.json")
            raise
        
        # 4. 데이터 파싱
        scriptures = fetcher.parse_bible_data(raw_data)
        
        if len(scriptures) == 0:
            print("❌ 파싱된 구절이 없습니다. JSON 구조를 확인하세요.")
            return
        
        # 5. DB에 저장
        fetcher.insert_to_db(scriptures)
        
        # 6. 검증
        fetcher.verify_data()
        
        print("\n" + "=" * 60)
        print("🎉 성경 데이터 수집 완료!")
        print("=" * 60)
        print("\n💡 다음 단계:")
        print("  1. python3 scripts/assign_characters.py  # 캐릭터 자동 할당")
        print("  2. n8n에서 complete_pipeline.json 실행")
        
    except Exception as e:
        print(f"\n❌ 에러 발생: {e}")
        import traceback
        traceback.print_exc()
    finally:
        fetcher.close()


if __name__ == "__main__":
    import sys
    
    # --file 옵션 지원
    if "--file" in sys.argv:
        file_index = sys.argv.index("--file")
        if len(sys.argv) > file_index + 1:
            filepath = sys.argv[file_index + 1]
            fetcher = BibleDataFetcher(DATABASE_URL)
            fetcher.connect_db()
            fetcher.add_unique_constraint()
            raw_data = fetcher.load_from_file(filepath)
            scriptures = fetcher.parse_bible_data(raw_data)
            fetcher.insert_to_db(scriptures)
            fetcher.verify_data()
            fetcher.close()
        else:
            print("❌ 사용법: python3 fetch_bible_data.py --file bible.json")
    else:
        main()
