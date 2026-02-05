import ffmpeg
import os
import logging
from ..config import Config

logger = logging.getLogger(__name__)

class FFmpegService:
    def __init__(self):
        self.output_dir = Config.OUTPUT_DIR
        self.temp_dir = Config.TEMP_DIR
        os.makedirs(self.temp_dir, exist_ok=True)

    def _get_temp_path(self, episode_id, suffix):
        return os.path.join(self.temp_dir, f"{episode_id}_{suffix}")

    def generate_motion_canvas(self, image_path: str, duration: float = 10.0, output_path: str = None, animation_mode: str = 'zoom_in') -> str:
        """
        [Motion Canvas V2]
        Converts a static image into a video with specific 'Ken Burns' effects.
        Modes: 'zoom_in', 'zoom_out', 'pan_left', 'pan_right', 'pan_up', 'pan_down'
        """
        if not output_path:
            filename = os.path.basename(image_path).split('.')[0]
            output_path = os.path.join(self.temp_dir, f"{filename}_motion.mp4")

        try:
            logger.info(f"Generating Motion Canvas ({animation_mode}) for: {image_path}")
            stream = ffmpeg.input(image_path, loop=1, t=duration)
            
            frames = int(duration * 30)
            
            if animation_mode == 'zoom_in':
                # Gentle Zoom In
                z_expr = f'min(zoom+0.0015,1.3)'
                x_expr = 'iw/2-(iw/zoom/2)'
                y_expr = 'ih/2-(ih/zoom/2)'
            elif animation_mode == 'zoom_out':
                # Simulate Zoom Out by starting zoomed in and zooming out is hard with zoompan start=1.
                # Alternative: Zoom In but REVERSE video? No, expensive.
                # Fallback: Slower Zoom In for "Static/Grand" feel.
                z_expr = f'min(zoom+0.0005,1.1)'
                x_expr = 'iw/2-(iw/zoom/2)'
                y_expr = 'ih/2-(ih/zoom/2)'
            elif animation_mode == 'pan_right': 
                # Camera moves Right (View moves Left)
                z_expr = '1.2'
                x_expr = f'(iw-iw/zoom) * (on/{frames})'
                y_expr = 'ih/2-(ih/zoom/2)'
            elif animation_mode == 'pan_left':
                # Camera moves Left (View moves Right)
                z_expr = '1.2'
                x_expr = f'(iw-iw/zoom) * (1 - on/{frames})'
                y_expr = 'ih/2-(ih/zoom/2)'
            elif animation_mode == 'pan_up': 
                # Camera moves Up (View moves Down) -> Start Bottom, End Top
                z_expr = '1.2'
                x_expr = 'iw/2-(iw/zoom/2)'
                y_expr = f'(ih-ih/zoom) * (1 - on/{frames})' 
            elif animation_mode == 'pan_down':
                # Camera moves Down (View moves Up) -> Start Top, End Bottom
                z_expr = '1.2'
                x_expr = 'iw/2-(iw/zoom/2)'
                y_expr = f'(ih-ih/zoom) * (on/{frames})'
            else: # Default Zoom In
                z_expr = f'min(zoom+0.0015,1.3)'
                x_expr = 'iw/2-(iw/zoom/2)'
                y_expr = 'ih/2-(ih/zoom/2)'

            stream = stream.filter(
                'zoompan',
                z=z_expr,
                d=frames,
                x=x_expr,
                y=y_expr,
                s='1280x720',
                fps=30
            )
            stream = stream.output(output_path, vcodec='libx264', pix_fmt='yuv420p', r=30, t=duration)
            stream.overwrite_output().run(capture_stdout=True, capture_stderr=True)
            return output_path
        except ffmpeg.Error as e:
            logger.error(f"Motion Canvas Error: {e.stderr.decode() if e.stderr else e}")
            raise

    def apply_cinematic_exposure(self, input_st, duration, intensity=0.5, frequency=2.0):
        expr = f"{intensity}*exp(-15*(mod(t,{frequency}))^2)"
        return input_st.filter('eq', brightness=expr)

    def compose_cinematic_sequence(
        self,
        episode_id: str,
        video_paths: list,
        audio_path: str,
        apply_exposure: bool = False
    ) -> str:
        """
        V4 Architecture: Multi-Clip Stitching (Robust Pre-render).
        1. Pre-render each clip to fixed 30fps, 1080p, specific duration.
        2. Stitch using Xfade.
        """
        logger.info(f"Starting Cinematic Composition for {episode_id} with {len(video_paths)} clips (Pre-render Mode)")
        
        final_out = os.path.join(self.output_dir, f"{episode_id}_final.mp4")
        
        if not audio_path or not os.path.exists(audio_path):
            logger.error("Audio path missing!")
            return None
            
        try:
            # 1. Get Audio Duration
            try:
                probe = ffmpeg.probe(audio_path)
                audio_duration = float(probe['format']['duration'])
            except Exception:
                audio_duration = 30.0
            
            logger.info(f"Audio Duration: {audio_duration}s")
            
            # 2. Calculation
            if not video_paths: raise ValueError("No videos")
            num_clips = len(video_paths)
            clip_duration = audio_duration / num_clips
            overlap = 1.0 
            
            # 3. Pre-render Clips
            prerendered_clips = []
            for i, path in enumerate(video_paths):
                seg_len = clip_duration + overlap
                if i == num_clips - 1: seg_len = clip_duration
                
                temp_clip = os.path.join(self.temp_dir, f"{episode_id}_seq{i}.mp4")
                
                # Robust Input + Filter Chain
                # stream_loop for inputs that might be short (like 5s Luma vs 12s needed)
                stream = ffmpeg.input(path, stream_loop=-1)
                stream = stream.filter('scale', 1280, 720, force_original_aspect_ratio='decrease')
                stream = stream.filter('pad', 1280, 720, '(ow-iw)/2', '(oh-ih)/2')
                stream = stream.filter('setsar', 1, 1)
                stream = stream.filter('fps', fps=30, round='up')
                
                if apply_exposure and i == int(num_clips / 2):
                     stream = self.apply_cinematic_exposure(stream, seg_len)

                stream = stream.filter('trim', duration=seg_len)
                stream = stream.filter('setpts', 'PTS-STARTPTS')
                
                stream.output(temp_clip, vcodec='libx264', r=30).overwrite_output().run()
                prerendered_clips.append(temp_clip)

            # 4. Xfade
            inputs = [ffmpeg.input(p) for p in prerendered_clips]
            if len(inputs) < 2:
                joined = inputs[0]
            else:
                stream = inputs[0]
                for i in range(1, len(inputs)):
                    offset = i * clip_duration
                    stream = ffmpeg.filter(
                        [stream, inputs[i]],
                        'xfade',
                        transition='fade',
                        duration=overlap,
                        offset=offset
                    )
                joined = stream
            
            # 5. Final Output
            audio = ffmpeg.input(audio_path)
            out = ffmpeg.output(joined, audio, final_out, vcodec='libx264', acodec='aac', shortest=None)
            out.overwrite_output().run(capture_stdout=True, capture_stderr=True)
            return final_out

        except ffmpeg.Error as e:
            logger.error(f"FFmpeg Error: {e.stderr.decode() if e.stderr else e}")
            raise
