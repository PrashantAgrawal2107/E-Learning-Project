from pydantic import BaseModel
from typing import Optional, List
from .questionSchema import QuestionCreate, QuestionResponse

class QuizBase(BaseModel):
    name: str
    description: Optional[str] = None

class QuizCreate(QuizBase):
    questions: List[QuestionCreate]
    # pass

class QuizUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    questions: Optional[List[QuestionCreate]] = None
    
class QuizResponse(QuizBase):
    id: int 
    questions: List[QuestionResponse]
    class Config:
        from_attributes = True