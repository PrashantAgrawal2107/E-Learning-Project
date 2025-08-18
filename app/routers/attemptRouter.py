from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..core.dbConfig import get_db
from ..schemas import attemptSchema
from ..services import attemptServices

router = APIRouter(prefix="/attempts", tags=["Attempts"])


@router.post("/")
def create_attempt(attempt: attemptSchema.AttemptCreate, db: Session = Depends(get_db)):
    return attemptServices.create_attempt(db, attempt)


@router.delete("/{attempt_id}")
def delete_attempt(attempt_id: int, db: Session = Depends(get_db)):
    return attemptServices.delete_attempt(db, attempt_id)


@router.get("/", response_model=list[attemptSchema.AttemptResponse])
def get_all_attempts(db: Session = Depends(get_db)):
    return attemptServices.get_all_attempts(db)


@router.get("/{attempt_id}", response_model=attemptSchema.AttemptResponse)
def get_attempt_by_id(attempt_id: int, db: Session = Depends(get_db)):
    return attemptServices.get_attempt_by_id(db, attempt_id)


@router.get("/student/{student_id}", response_model=list[attemptSchema.AttemptResponse])
def get_attempts_of_student(student_id: int, db: Session = Depends(get_db)):
    return attemptServices.get_attempts_of_student(db, student_id)


@router.get("/quiz/{quiz_id}", response_model=list[attemptSchema.AttemptResponse])
def get_attempts_on_quiz(quiz_id: int, db: Session = Depends(get_db)):
    return attemptServices.get_attempts_on_quiz(db, quiz_id)
