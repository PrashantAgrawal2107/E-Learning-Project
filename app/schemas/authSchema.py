# app/schemas/authSchema.py
from pydantic import BaseModel, EmailStr
from typing import Optional
from enum import Enum

class RoleEnum(str, Enum):
    student = "student"
    instructor = "instructor"

class LoginRequest(BaseModel):
    email: EmailStr
    password: str
    role: RoleEnum

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    sub: EmailStr
    role: RoleEnum

class RegisterRequest(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: Optional[RoleEnum] = "student"  # allow register as instructor too (if you want)
