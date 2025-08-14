from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime

# ---- Base schema ----
class StudentBase(BaseModel):
    name: str
    email: str
    password: str

    class Config:
        from_attributes = True 

# ---- Update schema ----
class StudentUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=100)
    email: Optional[EmailStr] = None
    password: Optional[str] = Field(None, min_length=6)

    class Config:
        from_attributes = True


# ---- Response schema ----
class StudentResponse(BaseModel):
    id: int
    name: str
    email: str
    created_on: datetime
    updated_on: datetime

    class Config:
        from_attributes = True