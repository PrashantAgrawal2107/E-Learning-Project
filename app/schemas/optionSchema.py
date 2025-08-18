from pydantic import BaseModel
from typing import Optional

class OptionBase(BaseModel):
    id: int
    description: Optional[str] = None
    is_correct: bool
    question_id: int  # Assuming this is the foreign key to the Question model

class OptionCreate(BaseModel):
    description: str
    is_correct: bool = False  # Default to False, backend can recalculate if needed

class OptionUpdate(BaseModel):
    description: Optional[str] = None
    is_correct: Optional[bool] = None
    
class OptionResponse(OptionBase):
    class Config:
        from_attributes = True