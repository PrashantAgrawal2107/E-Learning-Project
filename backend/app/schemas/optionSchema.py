from pydantic import BaseModel
from typing import Optional

class OptionBase(BaseModel):
    id: int
    description: Optional[str] = None
    is_correct: bool
    question_id: int  

class OptionCreate(BaseModel):
    description: str
    is_correct: bool = False 
    
class OptionUpdate(BaseModel):
    description: Optional[str] = None
    is_correct: Optional[bool] = None
    
class OptionResponse(BaseModel):
    id: int
    description: str
    is_correct: bool
    class Config:
        from_attributes = True