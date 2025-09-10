from pydantic import BaseModel
from typing import Optional, List
from .optionSchema import OptionCreate, OptionResponse

class QuestionBase(BaseModel):
    content: str

class QuestionCreate(QuestionBase):
    options: List[OptionCreate]

class QuestionUpdate(BaseModel):
    content: Optional[str] = None
    options: Optional[List[OptionCreate]] = None
    
class QuestionResponse(QuestionBase):
    id: int
    # content: int   // Ye error tha jisne dimaag kharaab kar diya bhaiiiiiii
    options: List[OptionResponse]
    class Config:
        from_attributes = True