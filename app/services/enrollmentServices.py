from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from ..models import enrollmentModel , studentModel , courseModel
from ..schemas import enrollmentSchema
from datetime import datetime, timezone


def create_enrollment(enrollment: enrollmentSchema.EnrollmentBase, db: Session, current_user):
    student = db.query(studentModel.Student).filter(studentModel.Student.id == enrollment.student_id).first()
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )

    course = db.query(courseModel.Course).filter(courseModel.Course.id == enrollment.course_id).first()
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )
    
    if current_user.role == "student" and current_user.id != student.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to enroll other student in this course"
        )
    
    if current_user.role == "instructor" and course.instructor_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to enroll students in this course"
        )

    existing = db.query(enrollmentModel.Enrollment).filter(
        enrollmentModel.Enrollment.student_id == enrollment.student_id,
        enrollmentModel.Enrollment.course_id == enrollment.course_id
    ).first()

    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Student already enrolled in this course"
        )

    db_enrollment = enrollmentModel.Enrollment(
        student_id=enrollment.student_id,
        course_id=enrollment.course_id,
        enroll_date=datetime.now(timezone.utc)
    )
    db.add(db_enrollment)
    db.commit()
    db.refresh(db_enrollment)
    return db_enrollment


def get_all_enrollments(db: Session):
    return db.query(enrollmentModel.Enrollment).all()

def get_enrollment_by_id(enrollment_id: int, db: Session):
    enrollment = db.query(enrollmentModel.Enrollment).filter(enrollmentModel.Enrollment.id == enrollment_id).first()
    if not enrollment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Enrollment not found"
        )
    return enrollment


def delete_enrollment(enrollment_id: int, db: Session, current_user):
    enrollment = db.query(enrollmentModel.Enrollment).filter(enrollmentModel.Enrollment.id == enrollment_id).first()
    if not enrollment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Enrollment not found"
        )
    
    student = db.query(studentModel.Student).filter(studentModel.Student.id == enrollment.student_id).first()
    course = db.query(courseModel.Course).filter(courseModel.Course.id == enrollment.course_id).first()

    if current_user.role == "student" and current_user.id != student.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to delete this enrollment"
        )
    
    if current_user.role == "instructor" and course.instructor_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to delete this enrollment"
        )

    db.delete(enrollment)
    db.commit()
    return {"message": "Enrollment deleted successfully"}


def get_courses_by_student(student_id: int, db: Session):
    student = db.query(studentModel.Student).filter(studentModel.Student.id == student_id).first()
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )
    
    enrollments = db.query(enrollmentModel.Enrollment).filter(enrollmentModel.Enrollment.student_id == student_id).all()
    courses = [enrollment.course for enrollment in enrollments] 
    return courses


def get_students_by_course(course_id: int, db: Session):
    course = db.query(courseModel.Course).filter(courseModel.Course.id == course_id).first()
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )
    
    enrollments = db.query(enrollmentModel.Enrollment).filter(enrollmentModel.Enrollment.course_id == course_id).all()
    students = [enrollment.student for enrollment in enrollments]
    return students
