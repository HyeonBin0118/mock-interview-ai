from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import SessionCreate, SessionOut
from app.services import interview
from app import models

router = APIRouter()


@router.post("/sessions", response_model=SessionOut)
def create_session(body: SessionCreate, db: Session = Depends(get_db)):
    try:
        session = interview.create_session(
            db=db,
            job_url=body.job_url,
            resume_text=body.resume_text,
        )
        return session
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/sessions/{session_id}", response_model=SessionOut)
def get_session(session_id: int, db: Session = Depends(get_db)):
    session = db.query(models.InterviewSession).filter(
        models.InterviewSession.id == session_id
    ).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return session