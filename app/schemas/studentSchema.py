from pydantic import BaseModel, EmailStr
from typing import Optional, List
from uuid import UUID
from .enrollmentSchema import EnrollmentOut

class StudentBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr

class StudentCreate(StudentBase):
    pass

class StudentUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    
class StudentOut(StudentBase):
    student_id: UUID
    enrollments: List[EnrollmentOut] = []
    class Config:
        from_attributes = True