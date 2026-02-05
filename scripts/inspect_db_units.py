import sys
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Add project root
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from video_processor.database import Scripture, StoryUnit, VerseToStory, StoryScene
from video_processor.config import Config

def inspect_units():
    engine = create_engine(Config.DATABASE_URL)
    SessionLocal = sessionmaker(bind=engine)
    db = SessionLocal()
    
    units = db.query(StoryUnit).all()
    print(f"Total StoryUnits: {len(units)}")
    for u in units:
        print(f"ID: {u.id} | Title: {u.title} | Status: {u.status} | Suno: {'Yes' if u.suno_url else 'No'}")
        verses = db.query(VerseToStory).filter(VerseToStory.story_unit_id == u.id).all()
        print(f"  Verses: {len(verses)}")
        scenes = db.query(StoryScene).filter(StoryScene.unit_id == u.id).all()
        print(f"  Scenes: {len(scenes)}")

if __name__ == "__main__":
    inspect_units()
