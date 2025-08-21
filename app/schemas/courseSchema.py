from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class CourseBase(BaseModel):
    name: str   
    description: Optional[str] = None

class CourseUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None

class ModuleInCourse(BaseModel):
    id: int
    name: str   
    description: Optional[str]

    class Config:
        from_attributes = True

class CourseResponse(CourseBase):
    id: int
    instructor_id: int
    duration: int
    created_on: datetime
    updated_on: datetime
    modules: List[ModuleInCourse] = []
    
    class Config:
        from_attributes = True
