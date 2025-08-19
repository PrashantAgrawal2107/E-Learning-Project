from pydantic import BaseModel, EmailStr , Field
from typing import Optional, List
from uuid import UUID
from .courseSchema import CourseResponse
from datetime import datetime

class InstructorBase(BaseModel):
    name: str
    email: EmailStr
    password: str

    class Config:
        from_attributes = True 

class   InstructorUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=100)
    email: Optional[EmailStr] = None
    password: Optional[str] = Field(None, min_length=6)

    class Config:
        from_attributes = True

class InstructorResponse(BaseModel):
    id: int
    name: str
    email: str
    role: str
    created_on: datetime
    updated_on: datetime
    courses: List[CourseResponse] = []

    class Config:
        from_attributes = True