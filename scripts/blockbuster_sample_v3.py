import asyncio
import os
import sys

# Add project root to path
sys.path.append(os.getcwd())

from video_processor.services.external_api_service import ExternalApiService
from video_processor.config import Config

async def main():
    api = ExternalApiService()
    # Refined safer prompt for Verse 3 (V3)
    prompt = (
        "A majestic brilliant light emerging in the deep cosmic void, lens flare, "
        "volumetric light rays filling the atmosphere, "
        "cinematic lighting, massive scale, deep atmospheric perspective, "
        "8k raw footage, cinematic tracking shot"
    )
    print(f"--- Generating Blockbuster Sample for Scene 3 (Light Birth) ---")
    print(f"Prompt: {prompt}")
    
    # This will trigger the updated ExternalApiService with blockbuster tags
    video_path = await api.generate_video_runway(prompt)
    
    if video_path and os.path.exists(video_path):
        print(f"\n[SUCCESS] Sample Video Generated at: {video_path}")
    else:
        print(f"\n[FAILURE] Video generation failed or returned fallback.")

if __name__ == "__main__":
    asyncio.run(main())
