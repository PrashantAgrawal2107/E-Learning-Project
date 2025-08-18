from typing import List, Optional
from pydantic import BaseModel

class AttemptAnswerBase(BaseModel):
    attempt_id: int
    question_id: int
    selected_option_id: int
    is_correct: Optional[bool] = False

class AttemptAnswerCreate(AttemptAnswerBase):
    pass

class AttemptAnswerUpdate(BaseModel):
    selected_option_id: Optional[int] = None
    is_correct: Optional[bool] = None

class AttemptAnswerResponse(AttemptAnswerBase):
    id: int

    class Config:
        from_attributes = True