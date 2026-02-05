import sys
import os
import asyncio
import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Add project root
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from video_processor.database import Base, Scripture, StoryUnit, VerseToStory
from video_processor.services.story_grouper import StoryGrouper
from video_processor.pipeline import Pipeline
from video_processor.config import Config

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def test_real_generation():
    engine = create_engine(Config.DATABASE_URL)
    SessionLocal = sessionmaker(bind=engine)
    db = SessionLocal()
    
    logger.info("--- 1. Grouping Verses (Real) ---")
    grouper = StoryGrouper(db)
    
    # Check if unit already exists to avoid re-grouping same thing
    # For now, let's just try to create next.
    unit = await grouper.create_next_story_unit()
    
    if not unit:
        # Maybe it's already grouped? Let's check pending story units
        unit = db.query(StoryUnit).filter(StoryUnit.status == "pending").first()
        if not unit:
            logger.info("No unit created/found. Check DB state.")
            return

    logger.info(f"✅ Processing Unit: {unit.title}")
    logger.info(f"   Range: {unit.verses_range}")
    logger.info(f"   ID: {unit.id}")
    
    logger.info("--- 2. Running Pipeline (Real APIs) ---")
    pipeline = Pipeline(db)
    
    # Ensure Manual Mode is FALSE if user wants to use Wrapper
    # Config keys are loaded from env, so it should be false if env updated
    logger.info(f"Suno Manual Mode: {Config.MANUAL_SUNO_MODE}")
    logger.info(f"Suno API URL: {Config.SUNO_API_URL}")
    
    await pipeline.process_story_unit(unit.id)
    
    # Check Result
    updated_unit = db.query(StoryUnit).get(unit.id)
    logger.info(f"✅ Pipeline Status: {updated_unit.status}")
    
    if updated_unit.status == "waiting_for_suno":
        print("\n" + "="*50)
        print("⏸  PAUSED FOR SUNO MUSIC GENERATION")
        print(f"Title: {unit.title}")
        print(f"Lyrics: {unit.phase3_vocal_lyrics[:100]}...")
        print("Please generate music manually, then resume.")
        print("="*50 + "\n")
    else:
        print("\n" + "="*50)
        print("🎉 PIPELINE COMPLETED (Or Failed/Started)")
        print(f"Status: {updated_unit.status}")
        print("="*50 + "\n")

    db.close()

if __name__ == "__main__":
    asyncio.run(test_real_generation())
