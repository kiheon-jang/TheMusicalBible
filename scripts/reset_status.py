import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from video_processor.database import StoryUnit

db_url = "sqlite:////Users/giheonjang/Documents/project/TMB/tmb.db"
engine = create_engine(db_url)
SessionLocal = sessionmaker(bind=engine)
db = SessionLocal()

unit = db.query(StoryUnit).order_by(StoryUnit.id.desc()).first()
if unit:
    print(f"Resetting Unit {unit.id} from {unit.status} to waiting_for_suno")
    unit.status = "waiting_for_suno"
    unit.final_video_path = None
    # unit.fish_url = None # Force regenerate
    # unit.hedra_url = None
    # We want to retry the flow after Suno.
    # Actually pipeline checks 'if fish_url: skip'. 
    # So we MUST clear fish_url and hedra_url to retry them.
    unit.fish_url = None
    unit.hedra_url = None
    unit.runway_url = None
    
    db.commit()
    print("Reset Complete.")
