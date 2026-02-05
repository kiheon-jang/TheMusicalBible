from fastapi import APIRouter, Depends, BackgroundTasks
from sqlalchemy.orm import Session
from ..database import get_db, Scripture
from ..pipeline import Pipeline

router = APIRouter()

@router.post("/generate")
async def trigger_generation(background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    """
    Triggers the generation pipeline for pending scriptures.
    """
    # 1. Use StoryGrouper to create a new unit from pending verses
    from ..services.story_grouper import StoryGrouper
    
    grouper = StoryGrouper(db)
    story_unit = await grouper.create_next_story_unit()
    
    if not story_unit:
        return {"status": "no_pending_items", "message": "No pending verses found to group."}

    # 2. Trigger Pipeline for the new StoryUnit
    pipeline = Pipeline(db)
    background_tasks.add_task(pipeline.process_story_unit, story_unit.id)

    return {
        "status": "triggered", 
        "unit_id": story_unit.id, 
        "title": story_unit.title,
        "message": f"Started processing: {story_unit.title} ({story_unit.verses_range})"
    }
