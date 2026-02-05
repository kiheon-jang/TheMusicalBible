import sys
import os

# Add current directory to sys.path to ensure module lookup works
sys.path.append(os.getcwd())

from video_processor.database import get_db, StoryUnit, StoryScene
from sqlalchemy.orm import Session
import logging

# Configure Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def clear_unit1_videos():
    db = next(get_db())
    try:
        unit_id = 1
        logger.info(f"Checking Unit {unit_id}...")
        
        unit = db.query(StoryUnit).filter(StoryUnit.id == unit_id).first()
        if not unit:
            logger.error(f"Unit {unit_id} not found!")
            return

        logger.info(f"Found Unit: {unit.title}. Clearing video_path for all scenes...")
        
        scenes = db.query(StoryScene).filter(StoryScene.unit_id == unit_id).all()
        for scene in scenes:
            if scene.video_path:
                logger.info(f"Clearing Scene {scene.sequence_order} video: {scene.video_path} -> None")
                scene.video_path = None
        
        # Also clear final path to force stitch
        unit.final_video_path = None
        unit.status = "processing_phase1" # Reset status to ensure pipeline picks it up
        
        db.commit()
        logger.info("Successfully CLEARED all video paths for Unit 1.")
        
    except Exception as e:
        logger.error(f"Error clearing videos: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    clear_unit1_videos()
