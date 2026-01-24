#!/usr/bin/env python3
"""
The Musical Bible (TMB) - 캐릭터 자동 할당
성경 본문에서 주요 캐릭터를 감지하여 character_main 필드에 할당
"""

import psycopg2
import os
import re

DATABASE_URL = os.getenv("DATABASE_URL") or "postgresql://user:password@localhost:5432/tmb"

# 캐릭터 매핑 규칙 (우선순위 순)
CHARACTER_MAPPING = [
    # 구약 주요 인물
    ("아브람|아브라함", "abraham"),
    ("사라|사래", "sarah"),
    ("이삭", "isaac"),
    ("리브가", "rebekah"),
    ("야곱|이스라엘", "jacob"),
    ("라헬", "rachel"),
    ("레아", "leah"),
    ("요셉", "joseph"),
    ("모세", "moses"),
    ("아론", "aaron"),
    ("미리암", "miriam"),
    ("여호수아", "joshua"),
    ("사무엘", "samuel"),
    ("사울", "saul"),
    ("다윗", "david"),
    ("솔로몬", "solomon"),
    ("엘리야", "elijah"),
    ("엘리사", "elisha"),
    ("이사야", "isaiah"),
    ("예레미야", "jeremiah"),
    ("에스겔", "ezekiel"),
    ("다니엘", "daniel"),
    ("욥", "job"),
    ("에스더", "esther"),
    ("룻", "ruth"),
    ("노아", "noah"),
    ("아담", "adam"),
    ("이브|하와", "eve"),
    
    # 신약 주요 인물
    ("예수|그리스도", "jesus"),
    ("마리아", "mary"),
    ("요셉", "joseph"),
    ("베드로|시몬", "peter"),
    ("바울|사울", "paul"),
    ("요한", "john"),
    ("야고보", "james"),
    ("안드레", "andrew"),
    ("빌립", "philip"),
    ("도마", "thomas"),
    ("마태", "matthew"),
    ("바돌로매", "bartholomew"),
    ("세례 요한|침례 요한", "john_baptist"),
    ("막달라 마리아", "mary_magdalene"),
]

def assign_characters(db_url: str, dry_run: bool = False):
    """
    성경 구절에서 캐릭터 감지 및 할당
    
    Args:
        db_url: PostgreSQL 연결 URL
        dry_run: True면 실제 업데이트 없이 결과만 출력
    """
    conn = psycopg2.connect(db_url)
    cursor = conn.cursor()
    
    print("=" * 60)
    print("🎭 캐릭터 자동 할당 시작")
    print("=" * 60)
    
    total_updated = 0
    
    for korean_pattern, english_name in CHARACTER_MAPPING:
        # 정규표현식으로 캐릭터 이름 매칭
        query = """
        SELECT COUNT(*)
        FROM scripture 
        WHERE korean_text ~ %s
          AND character_main IS NULL
          AND status = 'pending'
        """
        cursor.execute(query, (korean_pattern,))
        match_count = cursor.fetchone()[0]
        
        if match_count > 0:
            if not dry_run:
                # 실제 업데이트
                update_query = """
                UPDATE scripture 
                SET character_main = %s
                WHERE korean_text ~ %s
                  AND character_main IS NULL
                  AND status = 'pending'
                """
                cursor.execute(update_query, (english_name, korean_pattern))
                updated = cursor.rowcount
            else:
                updated = match_count
            
            if updated > 0:
                print(f"✅ {english_name:20s} : {updated:5d}개 구절")
                total_updated += updated
    
    if not dry_run:
        conn.commit()
        print("\n✅ DB 커밋 완료")
    else:
        conn.rollback()
        print("\n⚠️  Dry-run 모드: 실제 업데이트 없음")
    
    # 통계 출력
    cursor.execute("""
        SELECT 
            COUNT(*) FILTER (WHERE character_main IS NOT NULL) as with_character,
            COUNT(*) FILTER (WHERE character_main IS NULL) as without_character,
            COUNT(*) as total
        FROM scripture
        WHERE status = 'pending'
    """)
    stats = cursor.fetchone()
    
    print("\n" + "=" * 60)
    print("📊 캐릭터 할당 통계")
    print("=" * 60)
    print(f"  캐릭터 할당됨:  {stats[0]:,}개 구절")
    print(f"  캐릭터 없음:    {stats[1]:,}개 구절")
    print(f"  전체:           {stats[2]:,}개 구절")
    print(f"  할당률:         {stats[0]/stats[2]*100:.1f}%")
    
    # 캐릭터별 통계
    cursor.execute("""
        SELECT character_main, COUNT(*) as count
        FROM scripture
        WHERE character_main IS NOT NULL
          AND status = 'pending'
        GROUP BY character_main
        ORDER BY count DESC
        LIMIT 15
    """)
    top_characters = cursor.fetchall()
    
    print("\n🎬 캐릭터별 구절 수 (Top 15):")
    for char, count in top_characters:
        print(f"  {char:20s} : {count:5,}개")
    
    cursor.close()
    conn.close()
    
    print("\n🎉 캐릭터 할당 완료!")
    return total_updated


def main():
    import sys
    
    # --dry-run 옵션 확인
    dry_run = "--dry-run" in sys.argv
    
    if dry_run:
        print("⚠️  Dry-run 모드: 실제 업데이트 없이 결과만 확인합니다\n")
    
    try:
        total = assign_characters(DATABASE_URL, dry_run=dry_run)
        
        if not dry_run:
            print(f"\n✅ 총 {total:,}개 구절에 캐릭터 할당 완료!")
            print("\n💡 다음 단계:")
            print("  1. n8n에서 complete_pipeline.json 워크플로우 실행")
            print("  2. 순차적으로 영상 생성 시작 (창세기 1:1부터)")
        
    except Exception as e:
        print(f"\n❌ 에러 발생: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
