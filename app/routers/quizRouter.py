from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..core.dbConfig import get_db
from ..schemas.quizSchema import QuizCreate, QuizUpdate, QuizResponse
from ..services import quizServices

router = APIRouter(prefix="/quizzes", tags=["Quizzes"])


# Create Quiz (linked to module)
@router.post("/{module_id}", response_model=QuizResponse)
def create_quiz(module_id: int, quiz_data: QuizCreate, db: Session = Depends(get_db)):
    print('inrouter')
    return quizServices.create_quiz(db, quiz_data, module_id)


# Get all quizzes
@router.get("/", response_model=list[QuizResponse])
def get_all_quizzes(db: Session = Depends(get_db)):
    return quizServices.get_all_quizzes(db)


# Get quiz by ID
@router.get("/{quiz_id}", response_model=QuizResponse)
def get_quiz_by_id(quiz_id: int, db: Session = Depends(get_db)):
    quiz = quizServices.get_quiz_by_id(db, quiz_id)
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")
    return quiz


# Update quiz
@router.put("/{quiz_id}", response_model=QuizResponse)
def update_quiz(quiz_id: int, quiz_data: QuizUpdate, db: Session = Depends(get_db)):
    quiz = quizServices.update_quiz(db, quiz_id, quiz_data)
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")
    return quiz


# Delete quiz
@router.delete("/{quiz_id}")
def delete_quiz(quiz_id: int, db: Session = Depends(get_db)):
    quiz = quizServices.delete_quiz(db, quiz_id)
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")
    return {"message": "Quiz deleted successfully"}
