#!/usr/bin/env python3
"""
The Musical Bible (TMB) - 스토리 단위 분석
Claude를 사용하여 성경을 설교 단위(페리코페)로 그룹핑
"""

import anthropic
import psycopg2
import json
import os
import sys
from typing import List, Dict, Optional

CLAUDE_API_KEY = os.getenv("CLAUDE_API_KEY") or os.getenv("ANTHROPIC_API_KEY")
DATABASE_URL = os.getenv("DATABASE_URL") or "postgresql://user:password@localhost:5432/tmb"

class StoryUnitAnalyzer:
    def __init__(self, claude_api_key: str, db_url: str):
        self.client = anthropic.Anthropic(api_key=claude_api_key)
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
    
    def fetch_verses(self, book_name: str, chapter_start: int, chapter_end: int) -> List[tuple]:
        """DB에서 구절 가져오기"""
        query = """
            SELECT chapter, verse, korean_text
            FROM scripture
            WHERE book_name = %s
              AND chapter BETWEEN %s AND %s
            ORDER BY chapter, verse
        """
        self.cursor.execute(query, (book_name, chapter_start, chapter_end))
        return self.cursor.fetchall()
    
    def analyze_with_claude(self, book_name: str, verses: List[tuple]) -> Optional[Dict]:
        """Claude로 스토리 단위 분석"""
        
        # 구절 텍스트 준비
        verses_text = "\n".join([
            f"{v[0]}:{v[1]} {v[2]}" for v in verses
        ])
        
        prompt = f"""당신은 성경 설교학 및 내러티브 분석 전문가입니다.

다음 {book_name} 본문을 **설교 단위(페리코페)**로 나누어주세요.

## 입력 본문:
{verses_text}

## 그룹핑 원칙:
1. **완결된 스토리** (시작-전개-절정-결말)
2. **등장인물 일관성** (같은 캐릭터가 중심)
3. **장소/시간 연속성** (한 장면, 한 사건)
4. **설교 단위** (전통적 페리코페)
5. **영상 길이** (60-120초 권장, 최대 180초)
6. **주제 통일성** (하나의 핵심 메시지)

## 출력 형식 (JSON):
```json
{{
  "story_units": [
    {{
      "unit_id": 1,
      "verses_range": "1:1-5",
      "title": "빛의 창조",
      "verse_count": 5,
      "key_theme": "하나님이 빛을 만드심",
      "main_characters": ["하나님"],
      "story_arc": "하나님이 혼돈에서 빛을 분리하여 첫째 날을 창조",
      "estimated_duration_sec": 60,
      "split_reason": "첫째 날 창조 완결",
      "narrative_structure": {{
        "setup": "혼돈과 공허",
        "conflict": "어둠 속 혼란",
        "resolution": "빛의 분리와 질서"
      }}
    }}
  ]
}}
```

## 중요:
- 너무 짧게 나누지 마세요 (최소 3-5절)
- 너무 길게 묶지 마세요 (최대 30절)
- 설교자가 한 번의 설교로 다룰 수 있는 단위
- 뮤지컬 영상으로 만들 때 자연스러운 단위

지금 이 본문을 분석하세요."""

        try:
            message = self.client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=4000,
                messages=[{"role": "user", "content": prompt}]
            )
            
            response_text = message.content[0].text
            
            # JSON 추출
            import re
            json_match = re.search(r'```json\n(.*?)\n```', response_text, re.DOTALL)
            if json_match:
                result = json.loads(json_match.group(1))
                return result
            else:
                print("⚠️  JSON 형식을 찾을 수 없습니다")
                print(response_text)
                return None
                
        except Exception as e:
            print(f"❌ Claude 분석 실패: {e}")
            return None
    
    def save_story_units(self, book_name: str, story_units: List[Dict]):
        """스토리 단위를 DB에 저장"""
        
        for unit in story_units:
            try:
                self.cursor.execute("""
                    INSERT INTO story_units 
                    (book_name, verses_range, title, verse_count, 
                     key_theme, main_characters, story_arc, 
                     estimated_duration_sec, narrative_structure)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (book_name, verses_range) DO UPDATE
                    SET title = EXCLUDED.title,
                        key_theme = EXCLUDED.key_theme
                    RETURNING id
                """, (
                    book_name,
                    unit['verses_range'],
                    unit['title'],
                    unit['verse_count'],
                    unit['key_theme'],
                    json.dumps(unit['main_characters'], ensure_ascii=False),
                    unit['story_arc'],
                    unit['estimated_duration_sec'],
                    json.dumps(unit.get('narrative_structure', {}), ensure_ascii=False)
                ))
                
                story_id = self.cursor.fetchone()[0]
                print(f"  ✅ {book_name} {unit['verses_range']}: {unit['title']} (ID: {story_id})")
                
            except Exception as e:
                print(f"  ❌ 저장 실패: {e}")
        
        self.conn.commit()
    
    def analyze_book(self, book_name: str, total_chapters: int, batch_size: int = 5):
        """책 전체를 배치로 분석"""
        
        print(f"\n{'='*60}")
        print(f"📖 {book_name} 분석 시작 (총 {total_chapters}장)")
        print(f"{'='*60}")
        
        total_units = 0
        
        for start in range(1, total_chapters + 1, batch_size):
            end = min(start + batch_size - 1, total_chapters)
            
            print(f"\n🔍 {book_name} {start}-{end}장 분석 중...")
            
            # 구절 가져오기
            verses = self.fetch_verses(book_name, start, end)
            
            if not verses:
                print(f"  ⚠️  구절이 없습니다")
                continue
            
            print(f"  📝 {len(verses)}개 구절 로드됨")
            
            # Claude 분석
            result = self.analyze_with_claude(book_name, verses)
            
            if result and 'story_units' in result:
                units = result['story_units']
                print(f"  🎯 {len(units)}개 스토리 단위 식별됨")
                
                # DB 저장
                self.save_story_units(book_name, units)
                total_units += len(units)
            else:
                print(f"  ❌ 분석 실패")
        
        print(f"\n✅ {book_name} 완료: 총 {total_units}개 스토리 단위")
        return total_units
    
    def close(self):
        """연결 종료"""
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
        print("\n✅ DB 연결 종료")


def create_story_units_table(db_url: str):
    """story_units 테이블 생성"""
    conn = psycopg2.connect(db_url)
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS story_units (
          id SERIAL PRIMARY KEY,
          book_name VARCHAR(255) NOT NULL,
          verses_range VARCHAR(50) NOT NULL,
          title VARCHAR(255) NOT NULL,
          verse_count INTEGER NOT NULL,
          key_theme TEXT,
          main_characters JSONB,
          story_arc TEXT,
          estimated_duration_sec INTEGER,
          narrative_structure JSONB,
          
          -- 생성된 콘텐츠
          visual_prompt TEXT,
          vocal_prompt TEXT,
          music_prompt TEXT,
          
          -- API 결과
          suno_url TEXT,
          fish_url TEXT,
          hedra_url TEXT,
          runway_url TEXT,
          final_video_path TEXT,
          
          -- YouTube
          youtube_url TEXT,
          youtube_video_id VARCHAR(255),
          
          -- 상태
          status VARCHAR(50) DEFAULT 'pending',
          created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
          
          UNIQUE(book_name, verses_range)
        );
        
        CREATE INDEX IF NOT EXISTS idx_story_status ON story_units(status);
        CREATE INDEX IF NOT EXISTS idx_story_book ON story_units(book_name);
    """)
    
    conn.commit()
    cursor.close()
    conn.close()
    
    print("✅ story_units 테이블 생성 완료")


def main():
    """메인 실행 함수"""
    
    print("=" * 60)
    print("📖 The Musical Bible - 스토리 단위 분석")
    print("=" * 60)
    
    # 테이블 생성
    create_story_units_table(DATABASE_URL)
    
    # 분석기 초기화
    analyzer = StoryUnitAnalyzer(CLAUDE_API_KEY, DATABASE_URL)
    analyzer.connect_db()
    
    try:
        # 테스트: 창세기 1-5장만
        if "--test" in sys.argv:
            analyzer.analyze_book("창세기", 5, batch_size=5)
        
        # 창세기 전체
        elif "--genesis" in sys.argv:
            analyzer.analyze_book("창세기", 50, batch_size=5)
        
        # 전체 성경
        elif "--all" in sys.argv:
            books = [
                ("창세기", 50),
                ("출애굽기", 40),
                ("레위기", 27),
                ("민수기", 36),
                ("신명기", 34),
                # ... 전체 66권
            ]
            
            for book_name, chapters in books:
                analyzer.analyze_book(book_name, chapters)
        
        else:
            print("\n사용법:")
            print("  --test      : 창세기 1-5장 테스트")
            print("  --genesis   : 창세기 전체 (50장)")
            print("  --all       : 전체 성경 (66권)")
            print("\n예시:")
            print("  python3 analyze_story_units.py --test")
        
    except KeyboardInterrupt:
        print("\n\n⚠️  사용자 중단")
    except Exception as e:
        print(f"\n❌ 에러 발생: {e}")
        import traceback
        traceback.print_exc()
    finally:
        analyzer.close()


if __name__ == "__main__":
    if not CLAUDE_API_KEY or not CLAUDE_API_KEY.startswith("sk-ant-"):
        print("❌ CLAUDE_API_KEY 환경변수를 설정하세요")
        print("   export CLAUDE_API_KEY='sk-ant-...'")
        sys.exit(1)
    
    main()
