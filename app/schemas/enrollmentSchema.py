from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from datetime import datetime

class EnrollmentBase(BaseModel):
    student_id: int
    course_id: int
    progress: Optional[float] = 0.0

class EnrollmentCreate(EnrollmentBase):
    pass

class EnrollmentUpdate(BaseModel):
    progress: Optional[float] = None
    
class EnrollmentResponse(EnrollmentBase):
    id: int
    enroll_date: datetime
    class Config:
        from_attributes = True