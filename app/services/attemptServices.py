from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from ..models import attemptModel, attemptAnswerModel, quizModel, studentModel
from ..schemas import attemptSchema, attemptAnswerSchema


def create_attempt(db: Session, attempt_data: attemptSchema.AttemptCreate):
    # Validate student
    student = db.query(studentModel.Student).filter(studentModel.Student.id == attempt_data.student_id).first()
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Student with id {attempt_data.student_id} not found"
        )

    # Validate quiz
    quiz = db.query(quizModel.Quiz).filter(quizModel.Quiz.id == attempt_data.quiz_id).first()
    if not quiz:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Quiz with id {attempt_data.quiz_id} not found"
        )

    # Create attempt
    attempt = attemptModel.Attempt(
        student_id=attempt_data.student_id,
        quiz_id=attempt_data.quiz_id,
        score=attempt_data.score
    )
    db.add(attempt)
    db.commit()
    db.refresh(attempt)

    # Save attempt answers if provided
    if hasattr(attempt_data, "answers") and attempt_data.answers:
        for ans in attempt_data.answers:
            answer = attemptAnswerModel.AttemptAnswer(
                attempt_id=attempt.id,
                question_id=ans.question_id,
                selected_option_id=ans.selected_option_id,
                is_correct=ans.is_correct
            )
            db.add(answer)
        db.commit()

    db.refresh(attempt)
    return attempt


def delete_attempt(db: Session, attempt_id: int):
    attempt = db.query(attemptModel.Attempt).filter(attemptModel.Attempt.id == attempt_id).first()
    if not attempt:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Attempt with id {attempt_id} not found"
        )
    db.delete(attempt)
    db.commit()
    return {"message": f"Attempt {attempt_id} deleted successfully"}


def get_all_attempts(db: Session):
    return db.query(attemptModel.Attempt).all()


def get_attempt_by_id(db: Session, attempt_id: int):
    attempt = db.query(attemptModel.Attempt).filter(attemptModel.Attempt.id == attempt_id).first()
    if not attempt:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Attempt with id {attempt_id} not found"
        )
    return attempt


def get_attempts_of_student(db: Session, student_id: int):
    student = db.query(studentModel.Student).filter(studentModel.Student.id == student_id).first()
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Student with id {student_id} not found"
        )
    return db.query(attemptModel.Attempt).filter(attemptModel.Attempt.student_id == student_id).all()


def get_attempts_on_quiz(db: Session, quiz_id: int):
    quiz = db.query(quizModel.Quiz).filter(quizModel.Quiz.id == quiz_id).first()
    if not quiz:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Quiz with id {quiz_id} not found"
        )
    return db.query(attemptModel.Attempt).filter(attemptModel.Attempt.quiz_id == quiz_id).all()
