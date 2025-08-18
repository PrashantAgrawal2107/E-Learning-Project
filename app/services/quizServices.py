from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from ..models.quizModel import Quiz
from ..models.questionModel import Question
from ..models.optionModel import Option
from ..models.moduleModel import Module 
from ..schemas.quizSchema import QuizCreate, QuizUpdate


def create_quiz(db: Session, quiz_data: QuizCreate, module_id: int):

    print('entry')
    module = db.query(Module).filter(Module.id == module_id).first()
    if not module:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Module with id {module_id} not found"
        )
    print('module')

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

        if not q.options or len(q.options) < 2:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Each question must have at least 2 options"
            )

        if not any(opt.is_correct for opt in q.options):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Each question must have at least one correct option"
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


def get_all_quizzes(db: Session):
    return db.query(Quiz).all()


def get_quiz_by_id(db: Session, quiz_id: int):
    return db.query(Quiz).filter(Quiz.id == quiz_id).first()


def update_quiz(db: Session, quiz_id: int, quiz_data: QuizUpdate):
    quiz = db.query(Quiz).filter(Quiz.id == quiz_id).first()
    if not quiz:
        return None

    if quiz_data.title is not None:
        quiz.title = quiz_data.title
    if quiz_data.description is not None:
        quiz.description = quiz_data.description

    db.commit()
    db.refresh(quiz)
    return quiz


def delete_quiz(db: Session, quiz_id: int):
    quiz = db.query(Quiz).filter(Quiz.id == quiz_id).first()
    if not quiz:
        return None
    db.delete(quiz)
    db.commit()
    return quiz
