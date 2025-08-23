from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from ..models.quizModel import Quiz
from ..models.questionModel import Question
from ..models.optionModel import Option
from ..models.moduleModel import Module 
from ..schemas.quizSchema import QuizCreate, QuizUpdate
from ..models.instructorModel import Instructor
from ..models.enrollmentModel import Enrollment
from ..models.courseModel import Course
from ..auth.validations import sort_validation


def create_quiz(db: Session, quiz_data: QuizCreate, module_id: int, current_user: Instructor):

    module = db.query(Module).filter(Module.id == module_id).first()
    if not module:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Module with id {module_id} not found"
        )

    if not quiz_data.name or not quiz_data.name.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Quiz title cannot be empty"
        )

    if not quiz_data.questions or len(quiz_data.questions) == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Quiz must contain at least one question"
        )
    
    if module.course.instructor_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to create quiz inside this module"
        )


    quiz = Quiz(
        name=quiz_data.name.strip(),
        description=quiz_data.description.strip() if quiz_data.description else None,
        module_id=module_id
    )
    db.add(quiz)
    db.flush()  

    for q in quiz_data.questions:
       
        if not q.content or not q.content.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Question text cannot be empty"
            )

        if not q.options or len(q.options) < 2 or len(q.options) > 4:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Each question must have at 2-4 options"
            )
        
        correct_options = 0

        for opt in q.options:
            if opt.is_correct:
                correct_options+=1

        if correct_options!=1:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Each question must have one correct option"
            )

        question = Question(content=q.content.strip(), quiz=quiz)
        db.add(question)
        db.flush()  

        for opt in q.options:
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
    db.refresh(quiz)

    print('**',quiz)
    return quiz


def get_all_quizzes(db: Session, current_user, params):
    query = db.query(Quiz)

    if current_user.role == "instructor":
        courses = db.query(Course).filter(Course.instructor_id == current_user.id).all()
        course_ids = [c.id for c in courses]

        if not course_ids:
            return []

        query = query.join(Module).filter(Module.course_id.in_(course_ids))

    if current_user.role == "student":
        enrollments = db.query(Enrollment).filter(Enrollment.student_id == current_user.id).all()
        course_ids = [e.course_id for e in enrollments]

        if not course_ids:
            return []

        query = query.join(Module).filter(Module.course_id.in_(course_ids))

    valid_sort_fields = {
        "name": Quiz.name,
        "created_on": Quiz.created_on
    }

    sort_by = params.sort_by
    order = params.order
    skip = params.skip
    limit = params.limit    

    sort = sort_validation(valid_sort_fields, sort_by, order)

    if order.lower() == "desc":
        sort = sort.desc()
    else:
        sort = sort.asc()

    return query.order_by(sort).offset(skip*limit).limit(limit).all()

def get_quiz_by_id(db: Session, quiz_id: int, current_user):
    quiz = db.query(Quiz).filter(Quiz.id == quiz_id).first()

    if not quiz:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Quiz not found"
        )

    if current_user.role == "instructor":

        if quiz.module.course.instructor_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions to view this quiz"
            )

    if current_user.role == "student":
        enrolled_course_ids = [
            e.course_id for e in db.query(Enrollment)
                                  .filter(Enrollment.student_id == current_user.id)
                                  .all()
        ]

        if quiz.module.course_id not in enrolled_course_ids:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions to view this quiz"
            )

    return quiz


def update_quiz(db: Session, quiz_id: int, quiz_data: QuizUpdate, current_user: Instructor):
    quiz = db.query(Quiz).filter(Quiz.id == quiz_id).first()
    if not quiz:
        return None
    
    if quiz.module.course.instructor_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to update this quiz"
        )

    if quiz_data.name is not None:
        quiz.name = quiz_data.name
    if quiz_data.description is not None:
        quiz.description = quiz_data.description

    db.commit()
    db.refresh(quiz)
    return quiz


def delete_quiz(db: Session, quiz_id: int, current_user: Instructor):
    quiz = db.query(Quiz).filter(Quiz.id == quiz_id).first()
    if not quiz:
        return None
    
    if quiz.module.course.instructor_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to delete this quiz"
        )

    db.delete(quiz)
    db.commit()
    return quiz
