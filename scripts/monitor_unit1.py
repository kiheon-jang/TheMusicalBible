import sys
import os
import time
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from video_processor.database import StoryUnit
from video_processor.config import Config

def monitor_unit_1():
    db_url = "sqlite:////Users/giheonjang/Documents/project/TMB/tmb.db"
    engine = create_engine(db_url)
    SessionLocal = sessionmaker(bind=engine)
    
    print("👀 Monitoring Unit 1...")
    
    while True:
        db = SessionLocal()
        unit = db.query(StoryUnit).filter(StoryUnit.id == 1).first()
        db.close()
        
        if not unit:
            print("❌ Unit 1 Not Found in DB")
            break
            
        print(f"Status: {unit.status} | Video: {unit.final_video_path}")
        
        if unit.status == "completed":
            print(f"✅ Unit 1 COMPLETED! Video: {unit.final_video_path}")
            # Verify file exists
            if unit.final_video_path and os.path.exists(unit.final_video_path):
                print("🎥 Final video file exists.")
            else:
                print("⚠️ File path in DB but file missing on disk!")
            break
            
        if unit.status == "failed":
            print("❌ Unit 1 FAILED.")
            break
            
        time.sleep(5)

if __name__ == "__main__":
    monitor_unit_1()
