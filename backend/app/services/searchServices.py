from sqlalchemy.orm import Session
from sqlalchemy import or_
from ..models.studentModel import Student
from ..models.instructorModel import Instructor
from ..models.courseModel import Course
from ..models.moduleModel import Module
from ..models.quizModel import Quiz
from ..models.enrollmentModel import Enrollment

def search_students(db: Session, searchTerm: str):
    return db.query(Student).filter(
        or_(
            Student.name.ilike(f"%{searchTerm}%"),
            Student.email.ilike(f"%{searchTerm}%")
        )
    ).all()

def search_instructors(db: Session, searchTerm: str):
    return db.query(Instructor).filter(
        or_(
            Instructor.name.ilike(f"%{searchTerm}%"),
            Instructor.email.ilike(f"%{searchTerm}%")
        )
    ).all()

def search_courses(db: Session, searchTerm: str):
    return db.query(Course).filter(
        or_(
            Course.name.ilike(f"%{searchTerm}%"),
            Course.description.ilike(f"%{searchTerm}%")
        )
    ).all()

def search_all(db: Session, searchTerm: str):
    students = search_students(db, searchTerm)
    instructors = search_instructors(db, searchTerm)
    courses = search_courses(db, searchTerm)

    return {
        "students": students,
        "instructors": instructors,
        "courses": courses
    }

def search_dashboard(db: Session, searchTerm: str, current_user):
    results = {
        "courses": [],
        "modules": [],
        "quizzes": []
    }

    if current_user.role == "student":
        student = db.query(Student).filter(Student.id == current_user.id).first()
        if not student:
            return results

        enrolled_courses = [enrollment.course for enrollment in student.enrollments]

        courses = [
            course for course in enrolled_courses
            if searchTerm.lower() in course.name.lower() or
               (course.description and searchTerm.lower() in course.description.lower())
        ]

        modules = []
        quizzes = []
        for course in enrolled_courses:
            for module in course.modules:
                if searchTerm.lower() in module.name.lower() or \
                   (module.description and searchTerm.lower() in module.description.lower()):
                    modules.append(module)

                for quiz in module.quizzes:
                    if searchTerm.lower() in quiz.name.lower() or \
                       (quiz.description and searchTerm.lower() in quiz.description.lower()):
                        quizzes.append(quiz)

        results["courses"] = courses
        results["modules"] = modules
        results["quizzes"] = quizzes

    elif current_user.role == "instructor":
        instructor = db.query(Instructor).filter(Instructor.id == current_user.id).first()
        if not instructor:
            return results
        
        modules = db.query(Module).join(Module.course).filter(
            Course.instructor_id == instructor.id,
            or_(
                Module.name.ilike(f"%{searchTerm}%"),
                Module.description.ilike(f"%{searchTerm}%")
            )
        ).all()

        quizzes = []
        for module in modules:
            for quiz in module.quizzes:
                if searchTerm.lower() in quiz.name.lower() or \
                   (quiz.description and searchTerm.lower() in quiz.description.lower()):
                    quizzes.append(quiz)

        courses = db.query(Course).filter(
            Course.instructor_id == instructor.id,
            or_(
                Course.name.ilike(f"%{searchTerm}%"),
                Course.description.ilike(f"%{searchTerm}%")
            )
        ).all()

        results["courses"] = courses
        results["modules"] = modules
        results["quizzes"] = quizzes

    return results
