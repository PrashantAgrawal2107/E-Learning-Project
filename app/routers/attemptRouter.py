from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..core.dbConfig import get_db
from ..schemas import attemptSchema
from ..services import attemptServices
from ..auth.authentication import get_current_user, require_role
from ..models.studentModel import Student
from ..schemas.sortSchema import SortSchema

router = APIRouter(prefix="/attempts", tags=["Attempts"])


@router.post("/" ,  dependencies=[Depends(require_role("student"))])
def create_attempt(attempt: attemptSchema.AttemptCreate, db: Session = Depends(get_db),  current_user: Student = Depends(get_current_user)):
    return attemptServices.create_attempt(db, attempt, current_user)


@router.delete("/{attempt_id}",  dependencies=[Depends(require_role("student"))])
def delete_attempt(attempt_id: int, db: Session = Depends(get_db), current_user: Student = Depends(get_current_user)):
    return attemptServices.delete_attempt(db, attempt_id, current_user)


@router.get("/", response_model=list[attemptSchema.AttemptResponse])
def get_all_attempts(db: Session = Depends(get_db), current_user = Depends(get_current_user), params : SortSchema = Depends()):
    return attemptServices.get_all_attempts(db, current_user, params)


@router.get("/{attempt_id}", response_model=attemptSchema.AttemptResponse)
def get_attempt_by_id(attempt_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return attemptServices.get_attempt_by_id(db, attempt_id, current_user)


@router.get("/student/{student_id}", response_model=list[attemptSchema.AttemptResponse])
def get_attempts_of_student(student_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return attemptServices.get_attempts_of_student(db, student_id, current_user)


@router.get("/quiz/{quiz_id}", response_model=list[attemptSchema.AttemptResponse])
def get_attempts_on_quiz(quiz_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return attemptServices.get_attempts_on_quiz(db, quiz_id, current_user)
