from pydantic import BaseModel
from typing import Optional, List
from uuid import UUID
from .quizSchema import QuizCreate, QuizResponse

class ModuleBase(BaseModel):
    title: str
    description: Optional[str] = None
    content_url: Optional[str] = None  # PDF, video, text

class ModuleCreate(ModuleBase):
    quizzes: Optional[List[QuizCreate]] = []

class ModuleUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    content_url: Optional[str] = None
    quizzes: Optional[List[QuizCreate]] = None
    
class ModuleResponse(ModuleBase):
    module_id: UUID
    quizzes: List[QuizResponse] = []
    class Config:
        from_attributes = True