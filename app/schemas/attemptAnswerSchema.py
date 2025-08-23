from typing import Optional
from pydantic import BaseModel

class AttemptAnswerBase(BaseModel):
    attempt_id: int
    question_id: int
    selected_option_id: int
    is_correct: Optional[bool] = False

class AttemptAnswerCreate(BaseModel):
    question_id: int
    selected_option_id: int

class AttemptAnswerUpdate(BaseModel):
    selected_option_id: Optional[int] = None
    is_correct: Optional[bool] = None

class AttemptAnswerResponse(BaseModel):
    id: int
    question_id: int
    selected_option_id: int
    is_correct: bool
    class Config:
        from_attributes = True