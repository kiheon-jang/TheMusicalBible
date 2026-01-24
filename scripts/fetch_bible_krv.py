#!/usr/bin/env python3
"""
개역한글 성경 데이터 가져오기 (yuhwan/Bible-krv)
"""

import json
import requests
import psycopg2
import os

DATABASE_URL = os.getenv("DATABASE_URL") or "postgresql://postgres:cSdtWArmQfsLDSnpuKLoIgxHaRyGREXq@maglev.proxy.rlwy.net:15087/railway"

# GitHub 저장소
BASE_URL = "https://raw.githubusercontent.com/yuhwan/Bible-krv/master"

print("=" * 70)
print("📖 개역한글 성경 데이터 가져오기")
print("=" * 70)
print()

# 1. 책 목록 가져오기
print("📥 책 목록 다운로드 중...")
response = requests.get(f"{BASE_URL}/books.json")
books = response.json()
print(f"✅ {len(books)}권 확인")
print()

# 2. DB 연결
print("🔌 PostgreSQL 연결 중...")
conn = psycopg2.connect(DATABASE_URL)
cursor = conn.cursor()
print("✅ 연결 성공")
print()

# 3. 기존 데이터 삭제 (테스트 데이터)
print("🗑️  기존 테스트 데이터 삭제 중...")
cursor.execute("DELETE FROM scripture;")
conn.commit()
print("✅ 삭제 완료")
print()

# 4. 각 책 다운로드 및 삽입
total_verses = 0

for idx, book_name in enumerate(books, 1):
    print(f"📖 [{idx}/{len(books)}] {book_name} 다운로드 중...")
    
    try:
        # 책 데이터 다운로드
        book_url = f"{BASE_URL}/{book_name}.json"
        response = requests.get(book_url)
        chapters = response.json()
        
        # 각 장, 절 삽입
        verses_count = 0
        for chapter_num, verses in enumerate(chapters, 1):
            for verse_num, text in enumerate(verses, 1):
                cursor.execute("""
                    INSERT INTO scripture (book_name, chapter, verse, korean_text, status)
                    VALUES (%s, %s, %s, %s, 'pending')
                """, (book_name, chapter_num, verse_num, text))
                verses_count += 1
        
        conn.commit()
        total_verses += verses_count
        print(f"   ✅ {verses_count}개 구절 삽입")
        
    except Exception as e:
        print(f"   ❌ 오류: {e}")
        conn.rollback()

print()
print("=" * 70)
print(f"🎉 완료! 총 {total_verses:,}개 구절 삽입")
print("=" * 70)

# 5. 결과 확인
cursor.execute("SELECT book_name, COUNT(*) FROM scripture GROUP BY book_name ORDER BY MIN(id) LIMIT 10;")
print()
print("📊 샘플 확인 (처음 10권):")
for row in cursor.fetchall():
    print(f"  {row[0]}: {row[1]}개")

cursor.close()
conn.close()
