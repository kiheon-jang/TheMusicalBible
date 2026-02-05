import sys
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Add project root
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from video_processor.database import StoryScene
from video_processor.config import Config

def clear_scene_videos(unit_id):
    engine = create_engine(Config.DATABASE_URL)
    SessionLocal = sessionmaker(bind=engine)
    db = SessionLocal()
    
    scenes = db.query(StoryScene).filter(StoryScene.unit_id == unit_id).all()
    print(f"Clearing videos for {len(scenes)} scenes in Unit {unit_id}")
    for s in scenes:
        s.video_path = None
    
    db.commit()
    print("✅ Scene videos cleared.")

if __name__ == "__main__":
    clear_scene_videos(1)
