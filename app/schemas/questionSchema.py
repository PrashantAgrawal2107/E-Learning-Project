from pydantic import BaseModel
from typing import Optional, List
from uuid import UUID
from .optionSchema import OptionCreate, OptionResponse

class QuestionBase(BaseModel):
    text: str

class QuestionCreate(QuestionBase):
    options: List[OptionCreate]

class QuestionUpdate(BaseModel):
    text: Optional[str] = None
    options: Optional[List[OptionCreate]] = None
    
class QuestionReponse(QuestionBase):
    question_id: UUID
    options: List[OptionResponse]
    class Config:
        from_attributes = True