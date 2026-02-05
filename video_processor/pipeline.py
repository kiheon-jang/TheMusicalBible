import logging
import asyncio
import os
from sqlalchemy.orm import Session
from .database import Scripture, StoryUnit, VerseToStory, StoryScene
from .services import SunoService, ClaudeService, ExternalApiService, FFmpegService
from .config import Config

logger = logging.getLogger(__name__)

class Pipeline:
    def __init__(self, db: Session):
        self.db = db
        self.suno = SunoService()
        self.claude = ClaudeService()
        self.external = ExternalApiService()
        self.ffmpeg = FFmpegService()

    async def process_story_unit(self, unit_id: int):
        logger.info(f"START Processing StoryUnit ID: {unit_id} (V4 Cinematic Engine)")
        
        unit = self.db.query(StoryUnit).filter(StoryUnit.id == unit_id).first()
        if not unit:
            logger.error(f"StoryUnit {unit_id} not found")
            return

        try:
            # 1. Update Status
            unit.status = "processing_phase1"
            self.db.commit()

            # 2. Stage A: The Director (Claude)
            if not unit.scenes:
                logger.info("🎬 Director Mode: Generating Playbook...")
                
                verses = (
                    self.db.query(Scripture)
                    .join(VerseToStory, Scripture.id == VerseToStory.scripture_id)
                    .filter(VerseToStory.story_unit_id == unit.id)
                    .order_by(VerseToStory.order_in_story)
                    .all()
                )
                full_text = " ".join([v.korean_text for v in verses])
                
                playbook = await self.claude.generate_production_playbook(
                    full_text,
                    {"title": unit.title, "book": unit.book_name}
                ) or {}
                
                # Save Director's Vision
                unit.title = playbook.get("title", unit.title)
                unit.phase3_suno_prompt = playbook.get("musical_style", "Cinematic Orchestral")
                
                raw_lyrics = playbook.get("lyrics", full_text)
                if isinstance(raw_lyrics, dict):
                    # Convert dict to string (Key: Value\n)
                    unit.phase3_vocal_lyrics = "\n".join([f"[{k.upper()}] {v}" for k, v in raw_lyrics.items()])
                elif isinstance(raw_lyrics, list):
                    unit.phase3_vocal_lyrics = "\n".join(raw_lyrics)
                else:
                    unit.phase3_vocal_lyrics = str(raw_lyrics)
                
                # Create Scenes
                scenes_data = playbook.get("scenes", [])
                for s_data in scenes_data:
                     # Create DB Scene
                     new_scene = StoryScene(
                         unit_id=unit.id,
                         sequence_order=s_data.get("sequence", 1),
                         phase_type=s_data.get("phase", "context"),
                         visual_prompt=s_data.get("visual_prompt", "Cinematic scene")
                     )
                     self.db.add(new_scene)
                
                self.db.commit()
                logger.info(f"✅ Playbook Created: {len(scenes_data)} scenes defined.")

            # 3. Stage B: The Composer (Suno)
            logger.info("🎵 Composer Mode: Checking Music...")
            if unit.suno_url:
                logger.info("Skipping Suno (Already exists)")
            else:
                logger.info(f"Generating Music: {unit.phase3_suno_prompt}")
                suno_result = await self.suno.generate_music(
                    unit.phase3_suno_prompt, 
                    unit.phase3_vocal_lyrics, 
                    unit.title
                )
                
                if suno_result['status'] == 'manual_required':
                    logger.warning("Suno Manual Mode. Pausing for User Input.")
                    unit.status = "waiting_for_suno"
                    self.db.commit()
                    return # Stop here
                
                if suno_result.get('status') == 'completed': 
                     unit.suno_url = suno_result.get('url')
                     self.db.commit()

            # 4. Stage C: The Shoot (Runway Batch)
            logger.info("🎥 Production Mode: Shooting Scenes...")
            # Reload scenes
            scenes = self.db.query(StoryScene).filter(StoryScene.unit_id == unit.id).order_by(StoryScene.sequence_order).all()
            
            for scene in scenes:
                if scene.video_path:
                    logger.info(f"Scene {scene.sequence_order} already shot: {scene.video_path}")
                    continue
                
                logger.info(f"Shooting Scene {scene.sequence_order} (Phase: {scene.phase_type})...")
                
                # Expert Mode: Seed Management for Consistency (Optimization Strategy 3)
                # Successful seeds should be stored and varied. 
                # For now, we use a base seed (e.g. 777 for God) and add variation based on sequence.
                base_seed = 777 if unit.phase3_vocal_lyrics and "[GOD]" in unit.phase3_vocal_lyrics else 42
                seed = base_seed + (scene.sequence_order * 10) # Variation per scene
                
                # Image-to-Video (I2V) Priority (Optimization Strategy 1)
                # Check for Asset-based Master Image: assets/unit{id}/scene_{seq}.png
                image_url = None
                
                # Try finding a master image
                master_image_name = f"scene_{scene.sequence_order}.png"
                master_image_path = os.path.join("assets", f"unit_{unit.id}", master_image_name)
                
                # Check absolute path just in case
                if not os.path.exists(master_image_path):
                     # Try flattened structure or temp assets
                     master_image_path = os.path.join(Config.TEMP_DIR, f"unit{unit.id}_scene{scene.sequence_order}.png")
                     
                if os.path.exists(master_image_path):
                    logger.info(f"Using Master Image for Scene {scene.sequence_order}: {master_image_path}")
                    image_url = os.path.abspath(master_image_path)
                    
                    # 🎬 LUMA DREAM MACHINE MODE (Alternative B: Real Cinematic)
                    # Use Luma API for High-Quality Image-to-Video
                    logger.info(f"🎬 Luma Cinema Strategy: Shooting {os.path.basename(master_image_path)} via Luma API...")
                    
                    video_limit_prompt = scene.visual_prompt[:1000]
                    video_path = await self.external.generate_video_luma(
                        prompt=video_limit_prompt,
                        image_url=image_url
                    )
                else:
                    logger.info(f"No Master Image found for Scene {scene.sequence_order}. Fallback to Runway (Costly).")

                    video_limit_prompt = scene.visual_prompt[:1000]
                    video_path = await self.external.generate_video_runway(
                        video_limit_prompt, 
                        image_url=image_url, 
                        seed=seed
                    )
                
                if video_path:
                    scene.video_path = video_path
                    # Save seed for future variation
                    if hasattr(scene, 'seed'):
                        scene.seed = seed
                    self.db.commit()
                else:
                    logger.error(f"Failed to shoot Scene {scene.sequence_order}")

            # 5. Stage D: The Edit (Post-Production)
            logger.info("✂️ Editing Mode: Stitching Final Cut...")
            
            # Download Music
            suno_path = None
            if unit.suno_url:
                suno_path = await self.external.download_file(unit.suno_url, f"suno_{unit.id}.mp3")
            
            if not suno_path:
                logger.warning("Suno Audio missing. Using dummy for testing V4 flow.")
                suno_path = "tests/assets/dummy_music.mp3"

            # Collect Clips
            video_clips = [s.video_path for s in scenes if s.video_path]
            
            if not video_clips:
                logger.error("No video clips available for editing.")
                return

            # Final Stitch with Cinematic Exposure Effect
            final_path = self.ffmpeg.compose_cinematic_sequence(
                str(unit.id),
                video_clips,
                suno_path,
                apply_exposure=True # Blockbuster Mode: Pulse light at climax
            )
            
            if final_path:
                unit.final_video_path = final_path
                unit.status = "completed"
                self.db.commit()
                logger.info(f"🎉 TMB V4 Production COMPLETED. Premiere Ready: {final_path}")
            else:
                logger.error("Composition returned no path")
                unit.status = "failed_composition"
                self.db.commit()

        except Exception as e:
            logger.exception(f"Pipeline V4 Failed: {e}")
            unit.status = "failed"
            self.db.commit()

    async def resume_from_manual_suno(self, unit_id: int, suno_url: str):
        logger.info(f"Resuming StoryUnit {unit_id} with URL: {suno_url}")
        
        unit = self.db.query(StoryUnit).filter(StoryUnit.id == unit_id).first()
        if not unit: return

        unit.suno_url = suno_url
        unit.status = "processing_phase1"
        self.db.commit()
        
        await self.process_story_unit(unit_id)
