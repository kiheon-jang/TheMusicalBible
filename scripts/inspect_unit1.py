import sys
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from video_processor.database import StoryUnit
from video_processor.config import Config

def inspect_unit_1():
    db_url = "sqlite:////Users/giheonjang/Documents/project/TMB/tmb.db"
    engine = create_engine(db_url)
    SessionLocal = sessionmaker(bind=engine)
    db = SessionLocal()
    
    unit = db.query(StoryUnit).filter(StoryUnit.id == 1).first()
    if unit:
        print(f"Unit 1: {unit.title}")
        print(f"Status: {unit.status}")
        print(f"Suno URL: {unit.suno_url}")
        print(f"Runway URL: {unit.runway_url}")
        print(f"Hedra URL: {unit.hedra_url}")
        print(f"Final Path: {unit.final_video_path}")
    else:
        print("Unit 1 not found")

if __name__ == "__main__":
    inspect_unit_1()
