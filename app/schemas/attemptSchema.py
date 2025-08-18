from typing import List, Optional
from pydantic import BaseModel
from .attemptAnswerSchema import AttemptAnswerCreate, AttemptAnswerUpdate, AttemptAnswerResponse


class AttemptBase(BaseModel):
    quiz_id: int
    student_id: int
    score: Optional[int] = 0

class AttemptCreate(AttemptBase):
    answers: List[AttemptAnswerCreate]

class AttemptUpdate(BaseModel):
    score: Optional[int] = None
    answers: Optional[List[AttemptAnswerUpdate]] = None

class AttemptResponse(AttemptBase):
    id: int
    answers: List[AttemptAnswerResponse] = []

    class Config:
        orm_mode = True