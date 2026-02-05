import sys
import os
sys.path.append(os.getcwd())
from video_processor.database import SessionLocal, StoryUnit
import json

db = SessionLocal()
unit = db.query(StoryUnit).get(1)

if unit:
    print(f"Unit 1 Status: {unit.status}")
    print("Scenes:")
    scenes = sorted(unit.scenes, key=lambda x: x.sequence_order)
    for s in scenes:
        print(f" - Scene {s.sequence_order}: {s.video_path}")
else:
    print("Unit 1 not found")
db.close()
