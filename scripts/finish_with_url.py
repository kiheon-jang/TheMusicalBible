import sys
import os
import asyncio
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from video_processor.database import StoryUnit, StoryScene
from video_processor.pipeline import Pipeline

async def finish_with_url(unit_id: int, suno_url: str, force_luma: bool = True):
    db_url = "sqlite:////Users/giheonjang/Documents/project/TMB/tmb.db"
    engine = create_engine(db_url)
    SessionLocal = sessionmaker(bind=engine)
    db = SessionLocal()
    
    unit = db.query(StoryUnit).get(unit_id)
    if not unit:
        print(f"Unit {unit_id} not found")
        return

    print(f"Assigning URL {suno_url} to Unit {unit_id}")
    unit.suno_url = suno_url
    
    # We also update the lyrics/style to match the canonical user request 
    unit.phase3_suno_prompt = "Deep Male Baritone, God-like Voice, Epic Orchestral, Cinematic, Celestial, 30s Trailer Style, 120BPM"
    unit.phase3_vocal_lyrics = """[Male Lead Vocal]
[Intro]
태초에 하나님이 천지를 창조하시니라
땅이 혼돈하고 공허하며 흑암이 깊음 위에 있고
하나님의 신은 수면에 운행하시니라

[Verse]
하나님이 가라사대 빛이 있으라 하시매 빛이 있었고
그 빛이 하나님의 보시기에 좋았더라 하나님이 빛과 어둠을 나누사

[Powerful Chorus]
빛을 낮이라 칭하시고 어둠을 밤이라 칭하시니라
위대하신 주 하나님 세상을 창조하셨도다

[Outro]
저녁이 되며 아침이 되니 이는 첫째 날이니라
[End]"""
    
    
    if force_luma:
        print("FORCING LUMA RESET: Clearing existing video_paths...")
        if unit.scenes:
            for scene in unit.scenes:
                if scene.video_path:
                    print(f" - Clearing Scene {scene.sequence_order}: {scene.video_path} -> None")
                    scene.video_path = None
        unit.final_video_path = None
    
    # Reset enabled for I2V retry
    
    unit.status = "processing_phase1"
    
    db.commit()
    db.refresh(unit)

    pipeline = Pipeline(db)
    print(f"Starting Pipeline execution (Scenes: {len(unit.scenes)}, Bypassing Director)...")
    await pipeline.process_story_unit(unit.id)
    print("Pipeline Finished.")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python scripts/finish_with_url.py <unit_id> <suno_url>")
        sys.exit(1)
    
    id_arg = int(sys.argv[1])
    url_arg = sys.argv[2]
    asyncio.run(finish_with_url(id_arg, url_arg))
