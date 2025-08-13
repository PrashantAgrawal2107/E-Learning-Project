from pydantic import BaseModel
from typing import Optional
from uuid import UUID

class OptionBase(BaseModel):
    text: str
    is_correct: bool

class OptionCreate(OptionBase):
    pass

class OptionUpdate(BaseModel):
    text: Optional[str] = None
    is_correct: Optional[bool] = None
    
class OptionOut(OptionBase):
    option_id: UUID
    class Config:
        from_attributes = True