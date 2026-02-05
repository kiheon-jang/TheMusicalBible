import sys
import os
import asyncio
import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from video_processor.database import Base, Scripture
from video_processor.pipeline import Pipeline
from video_processor.config import Config

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Override Config for Test
Config.MANUAL_SUNO_MODE = True # Force manual mode to test waiting logic
Config.OUTPUT_DIR = "tests/output_e2e"
os.makedirs(Config.OUTPUT_DIR, exist_ok=True)

# Setup Test DB
engine = create_engine("sqlite:///:memory:") # Use in-memory SQLite for test
Base.metadata.create_all(engine)
SessionLocal = sessionmaker(bind=engine)

def seed_db(db):
    test_item = Scripture(
        book_name="Genesis",
        chapter=1,
        verse=1,
        korean_text="태초에 하나님이 천지를 창조하시니라",
        character_main="Narrator",
        emotion_primary="Grandeur",
        status="pending"
    )
    db.add(test_item)
    db.commit()
    return test_item.id

async def run_simulation():
    db = SessionLocal()
    item_id = seed_db(db)
    
    logger.info(f"--- 1. Triggering Pipeline for Item {item_id} ---")
    pipeline = Pipeline(db)
    
    # Run pipeline (should pause at Suno)
    await pipeline.process_scripture(item_id)
    
    item = db.query(Scripture).get(item_id)
    logger.info(f"Status after Phase 1: {item.status}")
    
    if item.status == "waiting_for_suno":
        logger.info("--- 2. Simulating User Manual Input ---")
        # Simulate user providing a Suno URL
        dummy_suno_url = "https://suno.com/song/dummy-123"
        
        # Resume pipeline
        await pipeline.resume_from_manual_suno(item_id, dummy_suno_url)
        
        item = db.query(Scripture).get(item_id)
        logger.info(f"Status after Resume: {item.status}")
        
    db.close()

if __name__ == "__main__":
    asyncio.run(run_simulation())
