from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from datetime import datetime

class EnrollmentBase(BaseModel):
    student_id: int
    course_id: int

class EnrollmentCreate(EnrollmentBase):
    pass

class EnrollmentUpdate(BaseModel):
    progress: int
    
class EnrollmentResponse(EnrollmentBase):
    id: int
    enroll_date: datetime
    progress: int
    class Config:
        from_attributes = True