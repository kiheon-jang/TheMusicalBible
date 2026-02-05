import sys
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Add project root
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from video_processor.database import StoryUnit, StoryScene
from video_processor.config import Config

def reset_unit(unit_id):
    engine = create_engine(Config.DATABASE_URL)
    SessionLocal = sessionmaker(bind=engine)
    db = SessionLocal()
    
    unit = db.query(StoryUnit).get(unit_id)
    if not unit:
        print(f"Unit {unit_id} not found")
        return

    print(f"Resetting Unit {unit_id}: {unit.title}")
    
    # Delete old scenes
    db.query(StoryScene).filter(StoryScene.unit_id == unit_id).delete()
    
    # Reset fields
    unit.status = "pending"
    unit.phase3_suno_prompt = None
    unit.phase3_vocal_lyrics = None
    unit.suno_url = None
    unit.final_video_path = None
    
    db.commit()
    print("✅ Unit reset successful.")

if __name__ == "__main__":
    reset_unit(1)
