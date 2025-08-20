from sqlalchemy.orm import Session
from sqlalchemy import or_
from ..models.studentModel import Student
from ..models.instructorModel import Instructor
from ..models.courseModel import Course

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
