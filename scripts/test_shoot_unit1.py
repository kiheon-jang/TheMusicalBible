import asyncio
import os
import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Add project root
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from video_processor.database import StoryUnit, StoryScene
from video_processor.services import ExternalApiService
from video_processor.config import Config

async def test_shoot(unit_id):
    engine = create_engine(Config.DATABASE_URL)
    SessionLocal = sessionmaker(bind=engine)
    db = SessionLocal()
    
    unit = db.query(StoryUnit).get(unit_id)
    scenes = db.query(StoryScene).filter(StoryScene.unit_id == unit_id).all()
    
    print(f"Testing shoot for Unit {unit_id}: {unit.title}")
    print(f"Scenes count: {len(scenes)}")
    
    external = ExternalApiService()
    
    for s in scenes:
        print(f"Shooting Scene {s.sequence_order}...")
        prompt = s.visual_prompt
        # Forced cinematic tags are added inside ExternalApiService
        video_path = await external.generate_video_runway(prompt, seed=777)
        print(f"Resulting path: {video_path}")
        if video_path and "runway_" in video_path:
            print("✅ Success: Generated Runway Video")
        else:
            print("⚠️ Fallback or Failure detected")

if __name__ == "__main__":
    asyncio.run(test_shoot(1))
