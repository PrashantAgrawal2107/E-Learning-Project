from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..core.dbConfig import get_db
from ..schemas.quizSchema import QuizCreate, QuizUpdate, QuizResponse
from ..services import quizServices
from ..auth.authentication import require_role, get_current_user
from ..models.instructorModel import Instructor

router = APIRouter(prefix="/quizzes", tags=["Quizzes"])

@router.post("/{module_id}", response_model=QuizResponse, dependencies=[Depends(require_role("instructor"))])
def create_quiz(module_id: int, quiz_data: QuizCreate, db: Session = Depends(get_db), current_user: Instructor = Depends(get_current_user)):
    return quizServices.create_quiz(db, quiz_data, module_id, current_user)


@router.get("/", response_model=list[QuizResponse])
def get_all_quizzes(db: Session = Depends(get_db)):
    return quizServices.get_all_quizzes(db)


@router.get("/{quiz_id}", response_model=QuizResponse)
def get_quiz_by_id(quiz_id: int, db: Session = Depends(get_db)):
    quiz = quizServices.get_quiz_by_id(db, quiz_id)
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")
    return quiz


@router.put("/{quiz_id}", response_model=QuizResponse, dependencies=[Depends(require_role("instructor"))])
def update_quiz(quiz_id: int, quiz_data: QuizUpdate, db: Session = Depends(get_db), current_user: Instructor = Depends(get_current_user)):
    quiz = quizServices.update_quiz(db, quiz_id, quiz_data, current_user)
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")
    return quiz



@router.delete("/{quiz_id}", dependencies=[Depends(require_role("instructor"))])
def delete_quiz(quiz_id: int, db: Session = Depends(get_db), current_user: Instructor = Depends(get_current_user)):
    quiz = quizServices.delete_quiz(db, quiz_id, current_user)
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")
    return {"message": "Quiz deleted successfully"}
