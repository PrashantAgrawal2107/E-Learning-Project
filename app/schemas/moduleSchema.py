from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ModuleBase(BaseModel):
    name: str
    duration: int
    description: Optional[str] = None
    content_url: Optional[str] = None
    course_id: int

    class Config:
        from_attributes = True


class ModuleUpdate(BaseModel):
    name: Optional[str] = None
    duration: Optional[int] = None
    description: Optional[str] = None
    content_url: Optional[str] = None

    class Config:
        from_attributes = True


class ModuleResponse(BaseModel):
    id: int
    name: str
    duration: int
    description: Optional[str] = None
    content_url: Optional[str] = None
    course_id: int
    created_on: datetime
    updated_on: datetime

    class Config:
        from_attributes = True