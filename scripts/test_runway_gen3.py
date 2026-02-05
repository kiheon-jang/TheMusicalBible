
import asyncio
import os
import sys
import logging

# Add project root to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from video_processor.services.external_api_service import ExternalApiService

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def main():
    logger.info(">>> Testing Runway Gen-3 Alpha Integration <<<")
    
    service = ExternalApiService()
    
    # Scene 1 Master Image
    image_path = "assets/unit1/scene_1.png"
    
    if not os.path.exists(image_path):
        logger.error(f"Image not found: {image_path}")
        return

    # Visual Script Prompt for Scene 1
    prompt = (
        "Cinematic shot of a massive, swirling ocean of dark matter in deep space. "
        "Viscous, heavy, chaotic fluid texture like black oil. "
        "Faint bioluminescent blue particles pulsing in the abyss. "
        "Slow rolling camera angle. IMAX 65mm, shallow depth of field, hyper-realistic, dark atmosphere, void."
    )
    
    logger.info(f"Target Image: {image_path}")
    logger.info(f"Prompt: {prompt}")

    # Generate
    try:
        video_path = await service.generate_video_runway(
            prompt=prompt,
            image_url=image_path,
            seed=None # Random seed
        )
        
        if video_path and os.path.exists(video_path):
            logger.info(">>> SUCCESS: Runway Gen-3 Generation Complete <<<")
            logger.info(f"Output: {video_path}")
        else:
            logger.error(">>> FAILED: Runway returned no video path. <<<")
            
    except Exception as e:
        logger.error(f"Runway Test Exception: {e}")

if __name__ == "__main__":
    asyncio.run(main())
