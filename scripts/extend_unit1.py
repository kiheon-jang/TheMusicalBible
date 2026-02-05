import sys
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from video_processor.database import StoryUnit, StoryScene, Scripture, VerseToStory
from video_processor.config import Config

def extend():
    db_url = "sqlite:////Users/giheonjang/Documents/project/TMB/tmb.db"
    engine = create_engine(db_url)
    SessionLocal = sessionmaker(bind=engine)
    db = SessionLocal()
    
    # 1. Get Verse 5
    v5 = db.query(Scripture).filter(Scripture.chapter==1, Scripture.verse==5).first()
    if not v5:
        print("Verse 5 not found")
        return

    # 2. Check if already linked
    existing = db.query(VerseToStory).filter(
        VerseToStory.story_unit_id == 1,
        VerseToStory.scripture_id == v5.id
    ).first()
    
    if not existing:
        print("Linking Verse 5...")
        link = VerseToStory(scripture_id=v5.id, story_unit_id=1, order_in_story=5)
        db.add(link)
        db.commit()
    else:
        print("Verse 5 already linked.")
        
    # 3. Update Lyrics
    # Correct Join
    verses = (
        db.query(Scripture)
        .join(VerseToStory, Scripture.id == VerseToStory.scripture_id)
        .filter(VerseToStory.story_unit_id == 1)
        .order_by(VerseToStory.order_in_story)
        .all()
    )
    
    full_text = ' '.join([v.korean_text for v in verses]).strip()
    print(f"Full Text ({len(verses)} verses): {full_text}")
    
    unit = db.query(StoryUnit).filter(StoryUnit.id == 1).first()
    unit.phase3_vocal_lyrics = full_text
    unit.verses_range = "1:1-5" # Update range label too
    db.commit()
    print("Unit 1 Lyrics Updated.")

if __name__ == "__main__":
    extend()
