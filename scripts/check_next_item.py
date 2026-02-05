import sys
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from video_processor.database import Scripture, BookOrder
from video_processor.config import Config

def check_next():
    engine = create_engine(Config.DATABASE_URL)
    SessionLocal = sessionmaker(bind=engine)
    db = SessionLocal()
    
    # Same logic as generation.py
    next_item = (
        db.query(Scripture)
        .join(BookOrder, Scripture.book_name == BookOrder.book_name_korean)
        .filter(Scripture.status == 'pending')
        .order_by(BookOrder.book_number, Scripture.chapter, Scripture.verse)
        .first()
    )
    
    if next_item:
        print(f"✅ Next Item: {next_item.book_name} {next_item.chapter}:{next_item.verse}")
        print(f"   Text: {next_item.korean_text}")
    else:
        print("❌ No pending items found!")
    
    db.close()

if __name__ == "__main__":
    check_next()
