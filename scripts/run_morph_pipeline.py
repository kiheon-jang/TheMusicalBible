import sys
import os
import asyncio
import logging

sys.path.append(os.getcwd())
from video_processor.services.external_api_service import ExternalApiService
from video_processor.config import Config

# Setup Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def run_morphing_pipeline():
    logger.info(">>> Starting Luma Morphing Pipeline (Infinity Loop) <<<")
    
    api_service = ExternalApiService()
    
    # 1. Define Master Image Paths (Unit 1, Scenes 1-5)
    # Ensure these exist!
    base_path = "assets/unit1"
    scenes = [
        os.path.join(base_path, "scene_1.png"),
        os.path.join(base_path, "scene_2.png"),
        os.path.join(base_path, "scene_3.png"),
        os.path.join(base_path, "scene_4.png"),
        os.path.join(base_path, "scene_5.png")
    ]
    
    # Check existence
    for p in scenes:
        if not os.path.exists(p):
            logger.error(f"Missing asset: {p}")
            return

    # 2. Define Transitions
    # We need 4 transitions for 5 scenes? 
    # Or should we do Scene 1 (Intro) -> Scene 1 to 2 -> Scene 2 to 3 ...
    # User wants "Continuous".
    # Let's do:
    # Segment 1: Scene 1 -> Scene 2 (Morph)
    # Segment 2: Scene 2 -> Scene 3 (Morph)
    # Segment 3: Scene 3 -> Scene 4 (Morph)
    # Segment 4: Scene 4 -> Scene 5 (Morph)
    # Segment 5: Scene 5 -> Scene 5 (Motion? or Fade Out) - Let's just do Motion for last one.
    
    tasks = []
    
    # Transition Prompts (Simplified for tests)
    prompts = [
        "Cinematic transition from void to light, genesis creation, slow morph, 8k resolution",
        "Cinematic transition from light to forming earth, separation of lands, god rays, 8k resolution",
        "Cinematic transition from earth to waters and plants, nature blooming, 8k resolution",
        "Cinematic transition to sun and moon, celestial bodies appearing, 8k resolution"
    ]
    
    results = []

    # Execute Sequentially to avoid rate limits? Or Parallel?
    # Luma might rate limit. Let's do sequential for safety and logging.
    
    for i in range(len(scenes) - 1):
        start_img = scenes[i]
        end_img = scenes[i+1]
        prompt = prompts[i] if i < len(prompts) else "Cinematic morph"
        
        logger.info(f"--- Generating Morph {i+1}: Scene {i+1} -> Scene {i+2} ---")
        video_path = await api_service.generate_video_luma(
            prompt=prompt,
            image_url=start_img,
            end_image_url=end_img
        )
        
        if video_path:
            logger.info(f"Morph {i+1} Success: {video_path}")
            results.append(video_path)
        else:
            logger.error(f"Morph {i+1} Failed.")
            return # Stop if chain breaks

    # Last Scene specific motion (No morph target)
    logger.info("--- Generating Final Scene Motion ---")
    last_video = await api_service.generate_video_luma(
        prompt="Cinematic ending, god-like view of creation, slow zoom out, 8k resolution",
        image_url=scenes[-1]
    )
    if last_video:
        results.append(last_video)
        
    logger.info("Pipeline Complete. Video Segments:")
    for r in results:
        logger.info(f" - {r}")

if __name__ == "__main__":
    asyncio.run(run_morphing_pipeline())
