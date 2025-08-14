from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from datetime import datetime

class EnrollmentBase(BaseModel):
    student_id: UUID
    course_id: UUID
    enrollment_date: Optional[datetime] = None
    progress: Optional[float] = 0.0

class EnrollmentCreate(EnrollmentBase):
    pass

class EnrollmentUpdate(BaseModel):
    progress: Optional[float] = None
    
class EnrollmentResponse(EnrollmentBase):
    enrollment_id: UUID
    class Config:
        from_attributes = True