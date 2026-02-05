import logging
import os
import sys

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from video_processor.database import get_db, StoryUnit, StoryScene

def reset_and_sync_scenes():
    db = next(get_db())
    unit_id = 1
    unit = db.query(StoryUnit).filter(StoryUnit.id == unit_id).first()
    
    if not unit:
        print(f"Unit {unit_id} not found.")
        return

    print(f"Resetting scenes for Unit {unit_id}...")
    
    # 1. Delete existing scenes
    db.query(StoryScene).filter(StoryScene.unit_id == unit_id).delete()
    db.commit()
    print("Deleted all existing scenes.")
    
    # 2. Create 5 Scenes matching our Master Images (Gen 1:1-5)
    scenes_data = [
        {"seq": 1, "phase": "intro", "prompt": "Genesis 1:1 - The Beginning. Void and Darkness."},
        {"seq": 2, "phase": "verse", "prompt": "Genesis 1:2 - Spirit hovering over the deep waters."},
        {"seq": 3, "phase": "verse", "prompt": "Genesis 1:3 - Let there be light. Explosion of light."},
        {"seq": 4, "phase": "verse", "prompt": "Genesis 1:4 - Separation of Light and Darkness."},
        {"seq": 5, "phase": "chorus", "prompt": "Genesis 1:5 - The First Day. Primitive Earth."}
    ]
    
    for s_data in scenes_data:
        new_scene = StoryScene(
            unit_id=unit.id,
            sequence_order=s_data["seq"],
            phase_type=s_data["phase"],
            visual_prompt=s_data["prompt"],
            video_path=None # Reset video path
        )
        db.add(new_scene)
        
    unit.status = "processing_phase1" # Ready to shoot
    db.commit()
    print("✅ Created 5 synchronized scenes.")

if __name__ == "__main__":
    reset_and_sync_scenes()
