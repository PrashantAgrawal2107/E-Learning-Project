from pydantic import BaseModel
from typing import Optional, List
from uuid import UUID
from .questionSchema import QuestionCreate, QuestionReponse

class QuizBase(BaseModel):
    title: str
    description: Optional[str] = None

class QuizCreate(QuizBase):
    questions: List[QuestionCreate]

class QuizUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    questions: Optional[List[QuestionCreate]] = None
    
class QuizResponse(QuizBase):
    quiz_id: UUID
    questions: List[QuestionReponse]
    class Config:
        from_attributes = True









