import sys
import os
import asyncio
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from video_processor.database import StoryUnit, StoryScene
from video_processor.config import Config
from video_processor.pipeline import Pipeline

async def resume():
    # Use Config.DATABASE_URL or hardcode for local
    db_url = "sqlite:////Users/giheonjang/Documents/project/TMB/tmb.db"
    engine = create_engine(db_url)
    SessionLocal = sessionmaker(bind=engine)
    db = SessionLocal()
    
    # metrics
    # Force Unit 1 check first
    unit = db.query(StoryUnit).filter(StoryUnit.id == 1).first()
    
    if unit:
         print(f"Forcing Unit 1 ID: {unit.id}, Status: {unit.status} to resume.")
         
         # V4 RESET Logic
         print("Performing V4 Full Reset (Clear Scenes, Music, Video)...")
         unit.status = "processing_phase1"
         unit.final_video_path = None
         unit.runway_url = None
         unit.suno_url = None # Force new 30s music generation
         
         # Delete existing scenes to force Playbook regeneration
         db.query(StoryScene).filter(StoryScene.unit_id == unit.id).delete()
         
         db.commit()
    
    pipeline = Pipeline(db)
    # We use process_story_unit directly now, not resume_from_manual_suno
    await pipeline.process_story_unit(unit.id)
    print("V4 Pipeline Triggered.")

if __name__ == "__main__":
    asyncio.run(resume())
