from pydantic import BaseModel
from typing import List, Optional


class QuestionOut(BaseModel):
    id: int
    category: str
    question_text: str
    model_answer: Optional[str]
    tip: Optional[str]
    difficulty: Optional[int]
    specificity: Optional[int]

    class Config:
        from_attributes = True


class SessionCreate(BaseModel):
    job_url: str
    resume_text: str


class SessionOut(BaseModel):
    id: int
    company: Optional[str]
    position: Optional[str]
    job_url: str
    questions: List[QuestionOut] = []

    class Config:
        from_attributes = True