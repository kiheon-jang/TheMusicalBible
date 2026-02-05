
import asyncio
import os
import sys
import logging

# Add project root to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from video_processor.services.ffmpeg_service import FFmpegService

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def main():
    logger.info(">>> Starting Motion Canvas Pipeline (FFmpeg Fallback) <<<")
    
    ffmpeg_service = FFmpegService()
    
    # 1. Define Scenes and Modes based on Visual Script
    scenes = [
        # Scene 1: Void -> Zoom In (Deep Dive)
        {
            "img": "assets/unit1/scene_1.png", 
            "mode": "zoom_in", 
            "desc": "Scene 1: Void (Zoom In)"
        },
        # Scene 2: Spirit -> Pan Right (Tracking)
        {
            "img": "assets/unit1/scene_2.png", 
            "mode": "pan_right", 
            "desc": "Scene 2: Spirit (Pan Right)"
        },
        # Scene 3: Light -> Zoom Out (Explosion/Impact)
        # We use zoom_out mode which simulates camera pulling back
        {
            "img": "assets/unit1/scene_3.png", 
            "mode": "zoom_out", 
            "desc": "Scene 3: Light (Zoom Out)"
        },
         # Scene 4: Division -> Pan Left (Separation)
        {
            "img": "assets/unit1/scene_4.png", 
            "mode": "pan_left", 
            "desc": "Scene 4: Division (Pan Left)"
        },
         # Scene 5: First Day -> Pan Up (Crane Up)
        {
            "img": "assets/unit1/scene_5.png", 
            "mode": "pan_up", 
            "desc": "Scene 5: First Day (Crane Up)"
        }
    ]

    # 2. Check Assets
    for s in scenes:
        if not os.path.exists(s["img"]):
            logger.error(f"Missing asset: {s['img']}")
            return

    # 3. Generate Motion Clips
    generated_clips = []
    # Total duration target? 
    # Let's assume standard length or check audio.
    # FFmpegService.compose_cinematic_sequence calculates duration based on audio.
    # But generate_motion_canvas needs a duration.
    # It's better to generate slightly longer clips (e.g. 10s) and let compose trim them.
    
    for i, s in enumerate(scenes):
        logger.info(f"--- Processing {s['desc']} ---")
        try:
            # Generate 12s clip to be safe
            clip_path = ffmpeg_service.generate_motion_canvas(
                image_path=s["img"], 
                duration=12.0, 
                animation_mode=s["mode"]
            )
            generated_clips.append(clip_path)
            logger.info(f"Generated: {clip_path}")
        except Exception as e:
            logger.error(f"Failed to animate {s['desc']}: {e}")
            return

    # 4. Stitch with Audio
    # Find Audio
    # We will search dynamically or hardcode if found.
    # Placeholder: assets/audio/unit1_audio.mp3 if not found later.
    audio_path = "assets/unit1/unit1_audio.mp3"  # Default guess
    # Check if exists, if not try to find one
    if not os.path.exists(audio_path):
         # Try common paths
         candidates = [
             "assets/voice/unit1_voice_music.mp3",
             "assets/unit1_voice_music.mp3",
             "assets/audio/unit1.mp3"
         ]
         for c in candidates:
             if os.path.exists(c):
                 audio_path = c
                 break
    
    if not os.path.exists(audio_path):
         # Try common paths
         candidates = [
             "assets/voice/unit1_voice_music.mp3",
             "assets/unit1_voice_music.mp3",
             "assets/audio/unit1.mp3",
             "output/temp/1_mixed_audio.mp3",
             "output/temp/unit1_mixed_audio.mp3"
         ]
         for c in candidates:
             if os.path.exists(c):
                 audio_path = c
                 break
    
    # Fallback: Search for any mixed audio in output/temp
    if not os.path.exists(audio_path):
        import glob
        temp_mixes = glob.glob("output/temp/*mixed_audio.mp3")
        if temp_mixes:
            audio_path = temp_mixes[0]
            
    if not os.path.exists(audio_path):
        logger.error(f"Audio not found at {audio_path}")


    logger.info(f"Using Audio: {audio_path}")

    try:
        final_video = ffmpeg_service.compose_cinematic_sequence(
            episode_id="unit1_motion_master",
            video_paths=generated_clips,
            audio_path=audio_path,
            apply_exposure=False 
        )
        logger.info(f"SUCCESS! Final Video: {final_video}")
    except Exception as e:
        logger.error(f"Composition Failed: {e}")

if __name__ == "__main__":
    asyncio.run(main())
