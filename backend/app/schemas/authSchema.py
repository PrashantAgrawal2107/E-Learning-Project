from pydantic import BaseModel, EmailStr
from typing import Optional
from enum import Enum
from datetime import datetime

class RoleEnum(str, Enum):
    student = "student"
    instructor = "instructor"

class LoginRequest(BaseModel):
    email: EmailStr
    password: str
    role: RoleEnum

class Token(BaseModel):
    access_token: str
    # token_type: str = "bearer"

class TokenData(BaseModel):
    sub: EmailStr
    role: RoleEnum


class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    role: str
    created_on: datetime
    updated_on: datetime
