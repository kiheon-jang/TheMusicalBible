import sys
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from video_processor.database import StoryUnit
from video_processor.config import Config

def show_details():
    engine = create_engine(Config.DATABASE_URL)
    SessionLocal = sessionmaker(bind=engine)
    db = SessionLocal()
    
    # Get the unit waiting for Suno
    unit = db.query(StoryUnit).filter(StoryUnit.status == "waiting_for_suno").first()
    
    if unit:
        print("\n" + "="*20 + " SUNO GENERATION DETAILS " + "="*20)
        print(f"📌 Title: {unit.title}")
        print(f"🎭 Style of Music: {unit.phase3_suno_prompt}")
        print("-" * 60)
        print(f"📜 Lyrics:\n{unit.phase3_vocal_lyrics}")
        print("="*60 + "\n")
    else:
        print("No unit is currently waiting for Suno.")
    
    db.close()

if __name__ == "__main__":
    show_details()
