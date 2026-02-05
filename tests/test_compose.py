import sys
import os
import logging

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from video_processor.services.ffmpeg_service import FFmpegService
from video_processor.config import Config

# Setup logging
logging.basicConfig(level=logging.INFO)

def test_pipeline():
    # 0. Override Config for Test
    Config.OUTPUT_DIR = "tests/output"
    Config.TEMP_DIR = "tests/output/temp"
    
    # 1. Init Service
    service = FFmpegService()
    
    # 2. Define Inputs (Assumes generate_dummy_assets.py ran)
    assets_dir = os.path.abspath("tests/assets")
    video_paths = {
        "phase1": os.path.join(assets_dir, "phase1.mp4"),
        "phase2": os.path.join(assets_dir, "phase2.mp4"),
        "phase3": os.path.join(assets_dir, "phase3.mp4"),
    }
    audio_paths = {
        "music": os.path.join(assets_dir, "music.mp3"),
        "voice": os.path.join(assets_dir, "voice.mp3"),
    }
    
    # 3. Running Composition
    print("Running FFmpegService.compose_video...")
    try:
        final_path = service.compose_video(
            episode_id="test_episode_001",
            scripture_text="태초에 하나님이 천지를 창조하시니라",
            book_info="창세기 1:1",
            video_paths=video_paths,
            audio_paths=audio_paths
        )
        print(f"\n✅ SUCCESS! Final video created at: {final_path}")
        print("Check if the video plays correctly with:")
        print("1. 0-8s: Black screen + Subtitles + Music (low)")
        print("2. 8-18s: Red screen + Music (rising)")
        print("3. 18-30s: Blue screen + Lip Sync (Voice+Music)")
        
    except Exception as e:
        print(f"\n❌ FAILED: {e}")

if __name__ == "__main__":
    test_pipeline()
