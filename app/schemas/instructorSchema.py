from pydantic import BaseModel, EmailStr
from typing import Optional, List
from uuid import UUID
from .courseSchema import CourseOut

class InstructorBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr

class InstructorCreate(InstructorBase):
    pass

class InstructorUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    
class InstructorOut(InstructorBase):
    instructor_id: UUID
    courses: List[CourseOut] = []
    class Config:
        from_attributes = True
