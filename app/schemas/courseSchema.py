from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class CourseBase(BaseModel):
    name: str   # updated for consistency
    description: Optional[str] = None
    duration: int 
    instructor_id: int 

class CourseUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    duration: Optional[int] = None

class ModuleInCourse(BaseModel):
    id: int
    name: str   # modulename → name
    description: Optional[str]

    class Config:
        from_attributes = True

class CourseResponse(CourseBase):
    id: int
    created_on: datetime
    updated_on: datetime
    modules: List[ModuleInCourse] = []
    
    class Config:
        from_attributes = True
