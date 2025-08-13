from pydantic import BaseModel
from typing import Optional, List
from uuid import UUID
from .optionSchema import OptionCreate, OptionOut

class QuestionBase(BaseModel):
    text: str

class QuestionCreate(QuestionBase):
    options: List[OptionCreate]

class QuestionUpdate(BaseModel):
    text: Optional[str] = None
    options: Optional[List[OptionCreate]] = None
    
class QuestionOut(QuestionBase):
    question_id: UUID
    options: List[OptionOut]
    class Config:
        from_attributes = True