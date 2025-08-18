from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..core.dbConfig import get_db
from ..schemas.questionSchema import QuestionUpdate, QuestionResponse
from ..services import questionServices

router = APIRouter(
    prefix="/questions",
    tags=["Questions"]
)

# 🔹 Update Question
@router.put("/{question_id}", response_model=QuestionResponse)
def update_question_endpoint(question_id: int, question_data: QuestionUpdate, db: Session = Depends(get_db)):
    return questionServices.update_question(db, question_id, question_data)


# 🔹 Delete Question
@router.delete("/{question_id}")
def delete_question_endpoint(question_id: int, db: Session = Depends(get_db)):
    return questionServices.delete_question(db, question_id)
