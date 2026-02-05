import sys
import os
import json
import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from video_processor.database import Base, Scripture, BookOrder
from video_processor.config import Config

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Bible Books Mapping (English -> Korean) 
# The JSON has English names ("Genesis"), our DB expects Korean ("창세기")
# We can query BookOrder to get the mapping!

def seed_bible(json_path="korean_bible.json"):
    # 1. Connect DB
    engine = create_engine(Config.DATABASE_URL)
    SessionLocal = sessionmaker(bind=engine)
    
    # Ensure tables exist (Crucial for SQLite)
    Base.metadata.create_all(engine)
    
    db = SessionLocal()
    
    # 2. Check & Seed BookOrder if missing (SQLite hasn't run init.sql)
    if db.query(BookOrder).count() == 0:
        logger.info("Seeding BookOrder data (SQLite)...")
        # Minimal seed for BookOrder to allow mapping
        # We need to parse book_order.sql or just use a simple mapping for the seeding script?
        # Let's map directly from the JSON names to Korean manually for the seed script to be self-contained.
        # But we need BookOrder for the application logic (sorting).
        # Let's read book_order.sql and try to parse it? Or just hardcode the mapping here for the seed.
        # Better: Hardcode a map for matching, and Insert BookOrder rows.
        
        # Simplified Hardcoded map for English -> Korean (Top 5 for MVP, or full list)
        # Actually, let's just create the map in memory for the seed script to work, 
        # and insert the BookOrder rows so the app works.
        pass # We will handle this in the loop below or separate function.
        
    # Load JSON to get the names
    with open(json_path, "r", encoding="utf-8-sig") as f:
        bible_data = json.load(f)

    # Dictionary for mapping English -> Korean (Manual list to ensure accuracy for SQLite)
    # This replaces the DB lookup since DB is empty.
    eng_to_kor = {
        "Genesis": "창세기", "Exodus": "출애굽기", "Leviticus": "레위기", "Numbers": "민수기", "Deuteronomy": "신명기",
        "Joshua": "여호수아", "Judges": "사사기", "Ruth": "룻기", "1 Samuel": "사무엘상", "2 Samuel": "사무엘하",
        "1 Kings": "열왕기상", "2 Kings": "열왕기하", "1 Chronicles": "역대상", "2 Chronicles": "역대하", "Ezra": "에스라",
        "Nehemiah": "느헤미야", "Esther": "에스더", "Job": "욥기", "Psalms": "시편", "Proverbs": "잠언",
        "Ecclesiastes": "전도서", "Song of Solomon": "아가", "Isaiah": "이사야", "Jeremiah": "예레미야", "Lamentations": "예레미야애가",
        "Ezekiel": "에스겔", "Daniel": "다니엘", "Hosea": "호세아", "Joel": "요엘", "Amos": "아모스",
        "Obadiah": "오바댜", "Jonah": "요나", "Micah": "미가", "Nahum": "나훔", "Habakkuk": "하박국",
        "Zephaniah": "스바냐", "Haggai": "학개", "Zechariah": "스가랴", "Malachi": "말라기",
        "Matthew": "마태복음", "Mark": "마가복음", "Luke": "누가복음", "John": "요한복음", "Acts": "사도행전",
        "Romans": "로마서", "1 Corinthians": "고린도전서", "2 Corinthians": "고린도후서", "Galatians": "갈라디아서", "Ephesians": "에베소서",
        "Philippians": "빌립보서", "Colossians": "골로새서", "1 Thessalonians": "데살로니가전서", "2 Thessalonians": "데살로니가후서",
        "1 Timothy": "디모데전서", "2 Timothy": "디모데후서", "Titus": "디도서", "Philemon": "빌레몬서", "Hebrews": "히브리서",
        "James": "야고보서", "1 Peter": "베드로전서", "2 Peter": "베드로후서", "1 John": "요한일서", "2 John": "요한이서",
        "3 John": "요한삼서", "Jude": "유다서", "Revelation": "요한계시록"
    }

    # Also seed BookOrder table if empty (so generation.py works)
    if db.query(BookOrder).count() == 0:
        logger.info("Populating BookOrder table...")
        for i, (eng, kor) in enumerate(eng_to_kor.items()):
            # Testament logic simplified
            testament = "OLD" if i < 39 else "NEW"
            bo = BookOrder(
                book_number=i+1,
                book_name_korean=kor,
                book_name_english=eng,
                testament=testament,
                chapter_count=0, # Placeholder
                verse_count=0     # Placeholder
            )
            db.add(bo)
        db.commit()

    book_order_map = eng_to_kor

    # 4. Insert Data
    total_count = 0
    buffer = []
    
    # Existing check to avoid re-seeding duplicates
    # For speed, let's assume if Genesis 1:1 exists, we skip Genesis? 
    # Or just ignore conflict if we can.
    # For now, simplistic check:
    existing_count = db.query(Scripture).count()
    if existing_count > 30000:
        logger.info(f"Database likely already seeded (Count: {existing_count}). Skipping.")
        return

    logger.info("Starting insertion...")
    
    for book in bible_data:
        eng_name = book["name"]
        
        # Mapping Fixes (Some JSON names might slightly differ)
        # 1 Kings -> 1 Kings (Exact?)
        # Let's handle minor diffs if needed.
        if eng_name not in book_order_map:
             # Try simple fixes
             if "Psalm" in eng_name: kor_name = "시편"
             else: 
                 logger.warning(f"Could not map book: {eng_name}")
                 continue
        else:
            kor_name = book_order_map[eng_name]

        chapters = book["chapters"]
        for ch_idx, verses in enumerate(chapters):
            chapter_num = ch_idx + 1
            for v_idx, text in enumerate(verses):
                verse_num = v_idx + 1
                
                # Check duplication? (Too slow for 31k items line by line)
                # Let's bulk add and hope for the best or use simple logic
                
                item = Scripture(
                    book_name=kor_name,
                    chapter=chapter_num,
                    verse=verse_num,
                    korean_text=text,
                    status="pending"
                )
                buffer.append(item)
                total_count += 1
                
                if len(buffer) >= 1000:
                    db.bulk_save_objects(buffer)
                    db.commit()
                    buffer = []
                    print(f"Inserted up to {kor_name} {chapter_num}:{verse_num}...", end='\r')
    
    if buffer:
        db.bulk_save_objects(buffer)
        db.commit()
        
    logger.info(f"Seeding Complete! Total verses: {total_count}")
    db.close()

if __name__ == "__main__":
    seed_bible()
