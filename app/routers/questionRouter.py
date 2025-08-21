from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..core.dbConfig import get_db
from ..schemas.questionSchema import QuestionUpdate, QuestionResponse
from ..services import questionServices
from ..auth.authentication import require_role, get_current_user
from ..models.instructorModel import Instructor

router = APIRouter(
    prefix="/questions",
    tags=["Questions"]
)


@router.put("/{question_id}", response_model=QuestionResponse, dependencies=[Depends(require_role("instructor"))])
def update_question_endpoint(question_id: int, question_data: QuestionUpdate, db: Session = Depends(get_db), current_user: Instructor = Depends(get_current_user)):
    return questionServices.update_question(db, question_id, question_data, current_user)


@router.delete("/{question_id}", dependencies=[Depends(require_role("instructor"))])
def delete_question_endpoint(question_id: int, db: Session = Depends(get_db), current_user: Instructor = Depends(get_current_user)):
    return questionServices.delete_question(db, question_id, current_user)
