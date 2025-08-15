from pydantic import BaseModel
from typing import Optional, List
from uuid import UUID
from .quizSchema import QuizCreate, QuizResponse

class ModuleBase(BaseModel):
    name: str
    duration: int
    description: Optional[str] = None
    content_url: Optional[str] = None  # PDF, video, text

class ModuleUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    content_url: Optional[str] = None
    quizzes: Optional[List[QuizCreate]] = None
    
class ModuleResponse(ModuleBase):
    id: int
    title: str
    quizzes: List[QuizResponse] = []
    class Config:
        from_attributes = True