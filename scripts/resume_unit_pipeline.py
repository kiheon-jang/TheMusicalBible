import sys
import os
import asyncio
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Add project root
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from video_processor.pipeline import Pipeline
from video_processor.config import Config

async def resume_pipeline(unit_id, suno_url):
    engine = create_engine(Config.DATABASE_URL)
    SessionLocal = sessionmaker(bind=engine)
    db = SessionLocal()
    
    pipeline = Pipeline(db)
    print(f"--- Resuming Pipeline for Unit {unit_id} with Suno URL ---")
    await pipeline.resume_from_manual_suno(unit_id, suno_url)
    print(f"--- Process Finished for Unit {unit_id} ---")
    
    db.close()

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python3 resume_unit_pipeline.py <unit_id> <suno_url>")
        sys.exit(1)
    
    u_id = int(sys.argv[1])
    s_url = sys.argv[2]
    asyncio.run(resume_pipeline(u_id, s_url))
