from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.questionModel import Question
from app.models.optionModel import Option
from app.schemas.questionSchema import QuestionUpdate, QuestionResponse

# 🔹 Update Question
def update_question(db: Session, question_id: int, question_data: QuestionUpdate):
    question = db.query(Question).filter(Question.id == question_id).first()
    if not question:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Question not found"
        )

    # update content
    if question_data.content:
        question.content = question_data.content

    # update options agar diye gaye hain
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

    question.options.clear()  # Clear existing options
    
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


# 🔹 Delete Question
def delete_question(db: Session, question_id: int):
    question = db.query(Question).filter(Question.id == question_id).first()
    if not question:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Question not found"
        )

    db.delete(question)
    db.commit()
    return {"message": "Question deleted successfully"}
