from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime

# ---- Base schema ----
class StudentBase(BaseModel):
    name: str = Field(..., max_length=100, description="Full name of the student")
    email: EmailStr = Field(..., description="Unique email address of the student")

    class Config:
        from_attributes = True 


# ---- Create schema ----
class StudentCreate(StudentBase):
    password: str = Field(..., min_length=6, description="Password for account")


# ---- Update schema ----
class StudentUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=100)
    email: Optional[EmailStr] = None
    password: Optional[str] = Field(None, min_length=6)

    class Config:
        from_attributes = True


# ---- Response schema ----
class StudentResponse(StudentBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True