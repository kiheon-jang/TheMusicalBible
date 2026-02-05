import sys
import os
import asyncio
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from video_processor.database import StoryUnit
from video_processor.config import Config

def check():
    db_url = "sqlite:////Users/giheonjang/Documents/project/TMB/tmb.db"
    engine = create_engine(db_url)
    SessionLocal = sessionmaker(bind=engine)
    db = SessionLocal()
    
    # Check Unit 1 specifically
    unit = db.query(StoryUnit).filter(StoryUnit.id == 1).first()
    print(f"Unit ID: {unit.id}")
    print(f"Status: {unit.status}")
    print(f"Suno URL: {unit.suno_url}")
    print(f"Final Video: {unit.final_video_path}")
    
    if unit.status == "completed":
        print("✅ Pipeline Success!")
    else:
        print("❌ Still missing something.")

if __name__ == "__main__":
    check()
