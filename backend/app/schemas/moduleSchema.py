from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class ModuleBase(BaseModel):
    name: str
    duration: int
    description: Optional[str] = None
    course_id: int

    class Config:
        from_attributes = True


class ModuleUpdate(BaseModel):
    name: Optional[str] = None
    duration: Optional[int] = None
    description: Optional[str] = None

    class Config:
        from_attributes = True

class QuizInModule(BaseModel):
    id: int
    name: str
    description: Optional[str] = None

    class Config:
        from_attributes = True

class ContentInModule(BaseModel):
    id: int
    file_name: str
    file_url: str
    file_type: Optional[str] = None

    class Config:
        from_attributes = True


class ModuleResponse(ModuleBase):
    id: int
    quizzes: List[QuizInModule] = []
    contents: List[ContentInModule] = []
    created_on: datetime
    updated_on: datetime

    class Config:
        from_attributes = True