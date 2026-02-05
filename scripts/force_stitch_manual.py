import sys
import os
sys.path.append(os.getcwd())
from video_processor.services.ffmpeg_service import FFmpegService

def stitch_manually():
    ffmpeg_service = FFmpegService()
    
    # Files identified from timestamp analysis
    video_paths = [
        "output/temp/luma_ab2af140-05e6-4dae-9c8b-b531a6b3b3d6.mp4", # Scene 1 (New, 15:28)
        "output/temp/luma_1ddfd3ad-b820-4dae-abaf-cc6877c41398.mp4", # Scene 2 (New, 15:31)
        "output/temp/luma_0567e6d7-d724-497a-acc2-1b4605373615.mp4", # Scene 3 (New, 15:33)
        "output/temp/luma_48c0ce3f-91f7-4a7f-bb7b-f48c8b128cbe.mp4", # Scene 4 (New, 15:35)
        "output/temp/luma_1259cb91-a7e4-4b4b-836c-f8ee68840181.mp4"  # Scene 5 (Old Best, 14:57)
    ]
    
    # Abs paths
    cwd = os.getcwd()
    abs_video_paths = [os.path.join(cwd, p) for p in video_paths]
    abs_audio_path = os.path.join(cwd, "output/temp/suno_1.mp3")
    
    print("Stitching paths:")
    for p in abs_video_paths:
        print(f" - {p} (Exists: {os.path.exists(p)})")
        
    print(f"Audio: {abs_audio_path} (Exists: {os.path.exists(abs_audio_path)})")
    
    output = ffmpeg_service.compose_cinematic_sequence(
        episode_id="1",
        video_paths=abs_video_paths,
        audio_path=abs_audio_path,
        apply_exposure=True
    )
    
    print(f"Comparison Done: {output}")

if __name__ == "__main__":
    stitch_manually()
