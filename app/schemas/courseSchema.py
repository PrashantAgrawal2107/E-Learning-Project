from pydantic import BaseModel
from typing import Optional, List
from uuid import UUID
from .moduleSchema import ModuleCreate, ModuleOut

class CourseBase(BaseModel):
    title: str
    description: Optional[str] = None
    category: Optional[str] = None

class CourseCreate(CourseBase):
    modules: Optional[List[ModuleCreate]] = []

class CourseUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    modules: Optional[List[ModuleCreate]] = None
    
class CourseOut(CourseBase):
    course_id: UUID
    modules: List[ModuleOut] = []
    class Config:
        from_attributes = True