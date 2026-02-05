import sys
import os
import asyncio
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Add project root
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from video_processor.database import Scripture, StoryUnit, VerseToStory, StoryScene
from video_processor.pipeline import Pipeline
from video_processor.config import Config

async def run_pipeline(unit_id):
    engine = create_engine(Config.DATABASE_URL)
    SessionLocal = sessionmaker(bind=engine)
    db = SessionLocal()
    
    pipeline = Pipeline(db)
    print(f"--- Running Pipeline for Unit {unit_id} ---")
    await pipeline.process_story_unit(unit_id)
    
    unit = db.query(StoryUnit).get(unit_id)
    print(f"--- Process Finished ---")
    print(f"Status: {unit.status}")
    print(f"Musical Style: {unit.phase3_suno_prompt}")
    print(f"Lyrics Generated: {'Yes' if unit.phase3_vocal_lyrics else 'No'}")
    
    db.close()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        u_id = int(sys.argv[1])
    else:
        u_id = 1
    asyncio.run(run_pipeline(u_id))
