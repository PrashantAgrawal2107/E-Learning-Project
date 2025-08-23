from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from ..models import attemptModel, attemptAnswerModel, quizModel, optionModel, questionModel, studentModel
from ..schemas import attemptSchema, attemptAnswerSchema
from ..models.studentModel import Student
from ..models.quizModel import Quiz
from ..models import moduleModel, courseModel
from ..models.enrollmentModel import Enrollment
from ..schemas import sortSchema
from ..auth.validations import sort_validation
from ..models.moduleModel import Module
from ..models.courseModel import Course

def create_attempt(db: Session, attempt_data: attemptSchema.AttemptCreate, current_user: Student):
    student = db.query(studentModel.Student).filter(studentModel.Student.id == attempt_data.student_id).first()
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Student with id {attempt_data.student_id} not found"
        )

    if current_user.id != attempt_data.student_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not allowed to create an attempt for this student"
        )

    quiz = db.query(quizModel.Quiz).filter(quizModel.Quiz.id == attempt_data.quiz_id).first()
    if not quiz:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Quiz with id {attempt_data.quiz_id} not found"
        )

    enrollment = (
        db.query(Enrollment)
        .filter(
            Enrollment.student_id == attempt_data.student_id,
            Enrollment.course_id == quiz.module.course_id
        )
        .first()
    )
    if not enrollment:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not enrolled in the course of this quiz"
        )

    attempt_count = (
        db.query(attemptModel.Attempt)
        .filter(
            attemptModel.Attempt.student_id == attempt_data.student_id,
            attemptModel.Attempt.quiz_id == attempt_data.quiz_id
        )
        .count()
    )

    if attempt_count >= 3:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You have already attempted this quiz 3 times. No more attempts allowed."
        )

    attempt = attemptModel.Attempt(
        student_id=attempt_data.student_id,
        quiz_id=attempt_data.quiz_id,
        score=0
    )
    db.add(attempt)
    db.flush()

    total_score = 0

    if hasattr(attempt_data, "answers") and attempt_data.answers:
        for ans in attempt_data.answers:
            question = (
                db.query(questionModel.Question)
                .filter(
                    questionModel.Question.id == ans.question_id,
                    questionModel.Question.quiz_id == attempt_data.quiz_id
                )
                .first()
            )
            if not question:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Question {ans.question_id} does not belong to quiz {attempt_data.quiz_id}"
                )

            selected_option = (
                db.query(optionModel.Option)
                .filter(
                    optionModel.Option.id == ans.selected_option_id,
                    optionModel.Option.question_id == ans.question_id
                )
                .first()
            )
            if not selected_option:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Invalid selected option {ans.selected_option_id} for question {ans.question_id}"
                )

            correct_option = (
                db.query(optionModel.Option)
                .filter(
                    optionModel.Option.question_id == ans.question_id,
                    optionModel.Option.is_correct == True
                )
                .first()
            )
            if not correct_option:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"No correct option found for question {ans.question_id}"
                )

            is_correct = ans.selected_option_id == correct_option.id
            if is_correct:
                total_score += 1

            answer = attemptAnswerModel.AttemptAnswer(
                attempt_id=attempt.id,
                question_id=ans.question_id,
                selected_option_id=ans.selected_option_id,
                is_correct=is_correct
            )
            db.add(answer)

    attempt.score = total_score
    db.commit()
    db.refresh(attempt)

    return attempt


def delete_attempt(db: Session, attempt_id: int, current_user: Student):
    attempt = db.query(attemptModel.Attempt).filter(attemptModel.Attempt.id == attempt_id).first()
    if not attempt:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Attempt with id {attempt_id} not found"
        )
    
    if attempt.student_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not allowed to delete this attempt"
        )

    db.delete(attempt)
    db.commit()
    return {"message": f"Attempt {attempt_id} deleted successfully"}


def get_all_attempts(db: Session, current_user, params: sortSchema):
    query = db.query(attemptModel.Attempt).join(attemptModel.Attempt.quiz).join(Quiz.module)

    if current_user.role == "instructor":
        query = query.join(Module.course).filter(Course.instructor_id == current_user.id)

    elif current_user.role == "student":
        enrolled_course_ids = [
            e.course_id for e in db.query(Enrollment)
                                  .filter(Enrollment.student_id == current_user.id)
                                  .all()
        ]
        query = query.filter(Module.course_id.in_(enrolled_course_ids))

    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Role not allowed to fetch attempts"
        )

    sort_by = params.sort_by
    order = params.order
    limit = params.limit
    skip = params.skip

    valid_sort_fields = {
        "id": attemptModel.Attempt.id,
        "quiz_id": attemptModel.Attempt.quiz_id,
        "score": attemptModel.Attempt.score,
        "created_on": attemptModel.Attempt.created_on
    }

    sort = sort_validation(valid_sort_fields,sort_by, order)

    return query.order_by(sort).offset(skip * limit).limit(limit).all()



def get_attempt_by_id(db: Session, attempt_id: int, current_user):
    attempt = (
        db.query(attemptModel.Attempt)
        .join(attemptModel.Attempt.quiz)
        .join(Quiz.module)
        .join(Module.course)
        .filter(attemptModel.Attempt.id == attempt_id)
        .first()
    )

    if not attempt:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Attempt with id {attempt_id} not found"
        )

    if current_user.role == "instructor":
        if attempt.quiz.module.course.instructor_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You are not allowed to access this attempt"
            )

    elif current_user.role == "student":
        enrolled_course_ids = [
            e.course_id for e in db.query(Enrollment)
                                  .filter(Enrollment.student_id == current_user.id)
                                  .all()
        ]
        if attempt.quiz.module.course_id not in enrolled_course_ids:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You are not allowed to access this attempt"
            )

    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Role not allowed to fetch attempt"
        )

    return attempt

def get_attempts_of_student(db: Session, student_id: int, current_user):
    student = db.query(studentModel.Student).filter(studentModel.Student.id == student_id).first()
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Student with id {student_id} not found"
        )

    if current_user.role == "student":
        if current_user.id != student_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You are not allowed to view other student's attempts"
            )

    elif current_user.role == "instructor":
        enrolled_course_ids = [
            e.course_id for e in db.query(Enrollment)
                                  .filter(Enrollment.student_id == student_id)
                                  .all()
        ]
        instructor_course_ids = [
            c.id for c in db.query(Course).filter(Course.instructor_id == current_user.id).all()
        ]

        if not any(c in instructor_course_ids for c in enrolled_course_ids):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You are not allowed to access this student's attempts"
            )

    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Role not allowed"
        )

    return db.query(attemptModel.Attempt).filter(attemptModel.Attempt.student_id == student_id).all()



def get_attempts_on_quiz(db: Session, quiz_id: int, current_user):
    quiz = db.query(quizModel.Quiz).filter(quizModel.Quiz.id == quiz_id).first()
    if not quiz:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Quiz with id {quiz_id} not found"
        )

    if current_user.role == "student":
        return db.query(attemptModel.Attempt).filter(
            attemptModel.Attempt.quiz_id == quiz_id,
            attemptModel.Attempt.student_id == current_user.id
        ).all()

    elif current_user.role == "instructor":
        if quiz.module.course.instructor_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You are not allowed to access attempts of this quiz"
            )
        return db.query(attemptModel.Attempt).filter(attemptModel.Attempt.quiz_id == quiz_id).all()

    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Role not allowed"
        )
