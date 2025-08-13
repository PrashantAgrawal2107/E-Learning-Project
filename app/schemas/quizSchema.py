from pydantic import BaseModel
from typing import Optional, List
from uuid import UUID
from .questionSchema import QuestionCreate, QuestionOut

class QuizBase(BaseModel):
    title: str
    description: Optional[str] = None

class QuizCreate(QuizBase):
    questions: List[QuestionCreate]

class QuizUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    questions: Optional[List[QuestionCreate]] = None
    
class QuizOut(QuizBase):
    quiz_id: UUID
    questions: List[QuestionOut]
    class Config:
        from_attributes = True









