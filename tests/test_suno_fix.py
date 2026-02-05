import sys
import os
import asyncio
import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from video_processor.services.suno_service import SunoService
from video_processor.config import Config

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def test_suno_direct():
    logger.info("--- Testing Suno Wrappper Fix ---")
    
    # Ensure Manual Mode is OFF
    Config.MANUAL_SUNO_MODE = False
    logger.info(f"Manual Mode: {Config.MANUAL_SUNO_MODE}")
    logger.info(f"API URL: {Config.SUNO_API_URL}")
    
    suno = SunoService()
    
    # Test Data
    prompt = "Cinematic orchestral, epic, grand" # tags
    lyrics = "[Verse]\nIn the beginning God created the heavens and the earth." # prompt
    title = "Test Genesis"
    
    logger.info("Sending request...")
    result = await suno.generate_music(prompt, lyrics, title)
    
    logger.info(f"Result: {result}")
    
    if result.get("status") == "started":
        logger.info("✅ SUCCESS! Suno Automation triggered.")
    else:
        logger.error("❌ FAILED. Still falling back to manual or error.")

if __name__ == "__main__":
    asyncio.run(test_suno_direct())
