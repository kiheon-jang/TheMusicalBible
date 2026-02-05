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

# Force SQLite for test just in case .env isn't picked up by some chance, 
# but Config should load it.
# Config.DATABASE_URL = "sqlite:///./tmb.db"

async def test_story_flow():
    engine = create_engine(Config.DATABASE_URL)
    SessionLocal = sessionmaker(bind=engine)
    
    # Ensure tables exist (including new StoryUnit)
    Base.metadata.create_all(engine)
    
    db = SessionLocal()
    
    logger.info("--- 1. Grouping Verses ---")
    grouper = StoryGrouper(db)
    unit = await grouper.create_next_story_unit()
    
    if not unit:
        logger.error("Failed to create story unit! Check if pending verses exist.")
        return

    logger.info(f"✅ Created Unit: {unit.title}")
    logger.info(f"   Range: {unit.verses_range}")
    logger.info(f"   ID: {unit.id}")
    
    # Check Verses
    verses = db.query(VerseToStory).filter(VerseToStory.story_unit_id == unit.id).all()
    logger.info(f"   Verse Count: {len(verses)}")

    logger.info("--- 2. Running Pipeline (Simulation) ---")
    pipeline = Pipeline(db)
    
    # Override Suno to Manual Mode to stop without error
    Config.MANUAL_SUNO_MODE = True
    
    await pipeline.process_story_unit(unit.id)
    
    # Check Result
    updated_unit = db.query(StoryUnit).get(unit.id)
    logger.info(f"✅ Pipeline Status: {updated_unit.status}")
    
    if updated_unit.status == "waiting_for_suno":
        logger.info("--- 3. Simulating Manual Resume ---")
        dummy_url = "https://suno.com/song/story-test-123"
        await pipeline.resume_from_manual_suno(unit.id, dummy_url)
        
        final_unit = db.query(StoryUnit).get(unit.id)
        logger.info(f"✅ Final Status: {final_unit.status}")
        logger.info(f"   Suno URL: {final_unit.suno_url}")

    db.close()

if __name__ == "__main__":
    asyncio.run(test_story_flow())
