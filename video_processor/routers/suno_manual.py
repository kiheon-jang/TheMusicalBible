from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from pydantic import BaseModel
from sqlalchemy.orm import Session
from ..database import get_db, Scripture
from ..pipeline import Pipeline

router = APIRouter()

class ManualSunoInput(BaseModel):
    episode_id: int
    suno_url: str

@router.post("/submit")
async def submit_manual_suno(input_data: ManualSunoInput, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    """
    Resumes pipeline with manual Suno URL.
    """
    item = db.query(Scripture).filter(Scripture.id == input_data.episode_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Episode not found")
        
    pipeline = Pipeline(db)
    background_tasks.add_task(pipeline.resume_from_manual_suno, input_data.episode_id, input_data.suno_url)
    
    return {"status": "resumed", "message": "Pipeline resumed with manual URL."}
