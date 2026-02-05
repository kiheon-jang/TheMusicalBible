import ffmpeg
import os


def generate_assets(output_dir="tests/assets"):
    os.makedirs(output_dir, exist_ok=True)
    
    # 1. Dummy Videos (Black, Red, Blue) - 10-15 seconds each
    print("Generating dummy videos...")
    colors = {
        "phase1": "black", 
        "phase2": "red", 
        "phase3": "blue"
    }
    
    for name, color in colors.items():
        try:
            (
                ffmpeg
                .input(f'color=c={color}:s=1280x720:d=15', f='lavfi')
                .output(os.path.join(output_dir, f"{name}.mp4"), vcodec='libx264', pix_fmt='yuv420p')
                .overwrite_output()
                .run(quiet=True)
            )
        except ffmpeg.Error as e:
            print(f"Failed to gen video {name}: {e}")

    # 2. Dummy Audio (Sine waves) - 60 seconds
    print("Generating dummy audio...")
    try:
        # Music (440Hz)
        (
            ffmpeg
            .input('sine=f=440:d=60', f='lavfi')
            .output(os.path.join(output_dir, "music.mp3"), acodec='libmp3lame')
            .overwrite_output()
            .run(quiet=True)
        )
        
        # Voice (880Hz)
        (
            ffmpeg
            .input('sine=f=880:d=60', f='lavfi')
            .output(os.path.join(output_dir, "voice.mp3"), acodec='libmp3lame')
            .overwrite_output()
            .run(quiet=True)
        )
    except ffmpeg.Error as e:
        print(f"Failed to gen audio: {e}")

    print("Assets generated in", output_dir)

if __name__ == "__main__":
    generate_assets()
