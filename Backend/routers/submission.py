from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List
from sqlalchemy.orm import Session
from database import get_db
from models import Submission

router = APIRouter()

# Pydantic model for submission
class SubmissionCreate(BaseModel):
    user_id: int
    assignment_id: int
    content: str

class SubmissionResponse(BaseModel):
    id: int
    user_id: int
    assignment_id: int
    content: str

    class Config:
        orm_mode = True

# Create a new submission
@router.post("/submissions/", response_model=SubmissionResponse)
def create_submission(submission: SubmissionCreate, db: Session = Depends(get_db)):
    new_submission = Submission(**submission.dict())
    db.add(new_submission)
    db.commit()
    db.refresh(new_submission)
    return new_submission

# Get all submissions
@router.get("/submissions/", response_model=List[SubmissionResponse])
def get_submissions(db: Session = Depends(get_db)):
    submissions = db.query(Submission).all()
    return submissions

# Get a submission by ID
@router.get("/submissions/{submission_id}", response_model=SubmissionResponse)
def get_submission(submission_id: int, db: Session = Depends(get_db)):
    submission = db.query(Submission).filter(Submission.id == submission_id).first()
    if not submission:
        raise HTTPException(status_code=404, detail="Submission not found")
    return submission