import sys
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from video_processor.database import StoryUnit, StoryScene
from video_processor.config import Config

def check():
    db_url = "sqlite:////Users/giheonjang/Documents/project/TMB/tmb.db"
    engine = create_engine(db_url)
    SessionLocal = sessionmaker(bind=engine)
    db = SessionLocal()
    
    unit = db.query(StoryUnit).filter(StoryUnit.id == 1).first()
    print(f"Unit 1 Title: {unit.title}")
    print(f"Lyrics Hook: {unit.phase3_vocal_lyrics[:50]}...")
    print(f"Music Style: {unit.phase3_suno_prompt}")
    
    scenes = db.query(StoryScene).filter(StoryScene.unit_id == 1).all()
    print(f"Scenes Count: {len(scenes)}")
    for s in scenes:
        print(f" - Scene {s.sequence_order} [{s.phase_type}]: {s.visual_prompt[:40]}...")

if __name__ == "__main__":
    check()
