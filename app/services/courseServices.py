from sqlalchemy.orm import Session
from .. import models, schemas
from fastapi import HTTPException, status

def create_course(course: schemas.CourseBase, db: Session):
    # Validate instructor exists
    instructor = db.query(models.Instructor).filter(models.Instructor.id == course.instructor_id).first()
    if not instructor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Instructor with id {course.instructor_id} does not exist"
        )
    db_course = models.Course(**course.model_dump())
    db.add(db_course)
    db.commit()
    db.refresh(db_course)
    return db_course

def get_all_courses(db: Session):
    return db.query(models.Course).all()

def get_course_by_id(course_id: int, db: Session):
    course = db.query(models.Course).filter(models.Course.id == course_id).first()
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )
    return course

def update_course(course_id: int, updated_course: schemas.CourseUpdate, db: Session):
    course = db.query(models.Course).filter(models.Course.id == course_id).first()
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )
    for key, value in updated_course.model_dump(exclude_unset=True).items():
        setattr(course, key, value)
    db.commit()
    db.refresh(course)
    return course

def delete_course(course_id: int, db: Session):
    course = db.query(models.Course).filter(models.Course.id == course_id).first()
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )
    db.delete(course)
    db.commit()
    return {"message": "Course deleted successfully"}