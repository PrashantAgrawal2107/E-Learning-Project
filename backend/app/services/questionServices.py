from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.questionModel import Question
from app.models.optionModel import Option
from app.schemas.questionSchema import QuestionUpdate, QuestionResponse
from ..models.instructorModel import Instructor

def update_question(db: Session, question_id: int, question_data: QuestionUpdate, current_user: Instructor):
    question = db.query(Question).filter(Question.id == question_id).first()
    if not question:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Question not found"
        )
    
    if question.quiz.module.course.instructor_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to update this question"
        )

    if question_data.content:
        question.content = question_data.content

    if not question_data.options or len(question_data.options) < 2:
        raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Each question must have at least 2 options"
            )    

    if not any(opt.is_correct for opt in question_data.options):
       raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Each question must have at least one correct option"
    )        

    question.options.clear()
    
    for opt in question_data.options:
        if not opt.description or not opt.description.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Option description cannot be empty"
            )
    
        option = Option(
            description=opt.description.strip(),
            is_correct=opt.is_correct,
            question_id=question.id 
        )
        db.add(option)      

    db.commit()
    db.refresh(question)
    return question


def delete_question(db: Session, question_id: int, current_user: Instructor):
    question = db.query(Question).filter(Question.id == question_id).first()
    if not question:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Question not found"
        )
    
    if question.quiz.module.course.instructor_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to delete this question"
        )

    db.delete(question)
    db.commit()
    return {"message": "Question deleted successfully"}
