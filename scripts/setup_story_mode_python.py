#!/usr/bin/env python3
"""
The Musical Bible - 스토리 모드 자동 설치 (Python 버전)
psql 없이도 실행 가능!
"""

import os
import sys
import subprocess
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

# 환경 변수 확인
DATABASE_URL = os.getenv("DATABASE_URL")
CLAUDE_API_KEY = os.getenv("CLAUDE_API_KEY")

if not DATABASE_URL:
    print(f"❌ DATABASE_URL 환경 변수가 설정되지 않았습니다")
    print("   Railway 대시보드에서 PostgreSQL 연결 문자열을 복사하세요")
    print()
    print("   설정 방법:")
    print("   export DATABASE_URL='postgresql://user:pass@host:port/railway'")
    sys.exit(1)

if not CLAUDE_API_KEY:
    print(f"❌ CLAUDE_API_KEY 환경 변수가 설정되지 않았습니다")
    print()
    print("   설정 방법:")
    print("   export CLAUDE_API_KEY='sk-ant-...'")
    sys.exit(1)

os.environ["DATABASE_URL"] = DATABASE_URL
os.environ["CLAUDE_API_KEY"] = CLAUDE_API_KEY

print("=" * 60)
print("📖 The Musical Bible - 스토리 모드 전환")
print("=" * 60)
print()

# Step 1: 패키지 설치 확인
print("━" * 60)
print("📦 Step 1/4: Python 패키지 확인")
print("━" * 60)

try:
    import anthropic
    import psycopg2
    import requests
    print("✅ 필요한 패키지 이미 설치됨")
except ImportError as e:
    print(f"📦 패키지 설치 중: {e.name}")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", "anthropic", "psycopg2-binary", "requests"])
    print("✅ 패키지 설치 완료")

print()

# Step 2: DB 연결 확인
print("━" * 60)
print("🔌 Step 2/4: 데이터베이스 연결 확인")
print("━" * 60)

try:
    conn = psycopg2.connect(DATABASE_URL)
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = conn.cursor()
    
    # 버전 확인
    cursor.execute("SELECT version();")
    version = cursor.fetchone()[0]
    print(f"✅ PostgreSQL 연결 성공")
    print(f"   {version.split(',')[0]}")
    
except Exception as e:
    print(f"❌ DB 연결 실패: {e}")
    sys.exit(1)

print()

# Step 3: 스키마 생성
print("━" * 60)
print("📊 Step 3/4: story_units 테이블 생성")
print("━" * 60)

schema_sql = """
-- story_units 테이블
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
  
  -- Claude 프롬프트 결과
  phase1_background_prompt TEXT,
  phase2_character_prompt TEXT,
  phase3_aria_prompt TEXT,
  music_prompt TEXT,
  music_style VARCHAR(100),
  emotion_tags JSONB,
  
  -- 계산된 타이밍
  phase1_duration_sec INTEGER,
  phase2_duration_sec INTEGER,
  phase3_duration_sec INTEGER,
  
  -- API 결과
  suno_music_url TEXT,
  suno_task_id VARCHAR(255),
  fish_audio_url TEXT,
  fish_task_id VARCHAR(255),
  hedra_video_url TEXT,
  hedra_character_id VARCHAR(255),
  runway_bg_url TEXT,
  runway_task_id VARCHAR(255),
  final_video_url TEXT,
  youtube_video_id VARCHAR(50),
  
  -- 메타데이터
  status VARCHAR(50) DEFAULT 'pending',
  error_message TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  
  UNIQUE(book_name, verses_range)
);

-- verse_to_story 매핑 테이블
CREATE TABLE IF NOT EXISTS verse_to_story (
  id SERIAL PRIMARY KEY,
  story_unit_id INTEGER REFERENCES story_units(id) ON DELETE CASCADE,
  scripture_id INTEGER REFERENCES scripture(id) ON DELETE CASCADE,
  order_in_story INTEGER,
  UNIQUE(story_unit_id, scripture_id)
);

-- 인덱스
CREATE INDEX IF NOT EXISTS idx_story_status ON story_units(status);
CREATE INDEX IF NOT EXISTS idx_story_book ON story_units(book_name);
CREATE INDEX IF NOT EXISTS idx_verse_to_story_unit ON verse_to_story(story_unit_id);
"""

try:
    cursor.execute(schema_sql)
    print("✅ story_units 테이블 생성 완료")
    
    # 테이블 확인
    cursor.execute("""
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'public' 
        AND table_name IN ('story_units', 'verse_to_story')
        ORDER BY table_name;
    """)
    tables = cursor.fetchall()
    for table in tables:
        print(f"   ✓ {table[0]}")
        
except Exception as e:
    print(f"❌ 스키마 생성 실패: {e}")
    sys.exit(1)

print()

# Step 4: 테스트 분석 실행
print("━" * 60)
print("🧪 Step 4/4: 테스트 분석 (창세기 1-5장)")
print("━" * 60)
print("⏳ 분석 시작... (약 2-3분 소요)")
print()

try:
    result = subprocess.run(
        [sys.executable, "scripts/analyze_story_units.py", "--test"],
        capture_output=True,
        text=True,
        timeout=300
    )
    
    if result.returncode == 0:
        print(result.stdout)
        print("✅ 스토리 분석 완료")
    else:
        print(f"⚠️  분석 중 경고: {result.stderr}")
        if "successfully" in result.stdout.lower():
            print("✅ 일부 성공")
        
except subprocess.TimeoutExpired:
    print("⚠️  타임아웃 (5분 초과)")
except Exception as e:
    print(f"⚠️  분석 오류: {e}")

print()

# Step 5: 결과 확인
print("━" * 60)
print("📊 결과 확인")
print("━" * 60)

try:
    # 통계
    cursor.execute("SELECT COUNT(*) FROM story_units;")
    total_stories = cursor.fetchone()[0]
    
    cursor.execute("SELECT SUM(verse_count) FROM story_units;")
    total_verses_result = cursor.fetchone()[0]
    total_verses = total_verses_result if total_verses_result else 0
    
    cursor.execute("SELECT ROUND(AVG(estimated_duration_sec)) FROM story_units;")
    avg_duration_result = cursor.fetchone()[0]
    avg_duration = int(avg_duration_result) if avg_duration_result else 0
    
    print()
    print("📊 통계:")
    print(f"  - 총 스토리: {total_stories} 개")
    print(f"  - 총 구절: {total_verses} 개")
    print(f"  - 평균 길이: {avg_duration} 초")
    print()
    
    # 샘플 데이터
    if total_stories > 0:
        cursor.execute("""
            SELECT id, book_name, verses_range, title, verse_count 
            FROM story_units 
            ORDER BY id 
            LIMIT 5;
        """)
        stories = cursor.fetchall()
        
        print("📖 생성된 스토리 (처음 5개):")
        for story in stories:
            print(f"  {story[0]}. {story[1]} {story[2]}: {story[3]} ({story[4]}절)")
    
except Exception as e:
    print(f"⚠️  통계 조회 오류: {e}")

finally:
    cursor.close()
    conn.close()

print()
print("━" * 60)
print("🎉 설치 완료!")
print("━" * 60)
print()
print("💡 다음 단계:")
print()
print("1. n8n 워크플로우 임포트:")
print("   - Railway n8n 대시보드 열기")
print("   - 'Import' 클릭")
print("   - workflows/complete_pipeline_story.json 선택")
print("   - Credentials 연결")
print()
print("2. 추가 분석 (선택):")
print("   python3 scripts/analyze_story_units.py --genesis  # 창세기 전체")
print("   python3 scripts/analyze_story_units.py --all      # 전체 성경")
print()
print("3. 테스트 실행:")
print("   - n8n에서 'Execute Workflow' 클릭")
print("   - 첫 스토리 영상 생성 확인")
print()
print("=" * 60)
