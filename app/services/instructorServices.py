from sqlalchemy.orm import Session
from .. import models, schemas
from fastapi import HTTPException, status

def create_instructor(instructor: schemas.InstructorCreate, db: Session):
    db_instructor = models.Instructor(**instructor.model_dump())
    db.add(db_instructor)
    db.commit()
    db.refresh(db_instructor)
    return db_instructor

def get_all_instructors(db: Session):
    return db.query(models.Instructor).all()

def get_instructor_by_id(instructor_id: int, db: Session):
    instructor = db.query(models.Instructor).filter(models.Instructor.id == instructor_id).first()
    if not instructor:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Instructor not found")
    return instructor

def update_instructor(instructor_id: int, updated_instructor: schemas.InstructorUpdate, db: Session):
    instructor = db.query(models.Instructor).filter(models.Instructor.id == instructor_id).first()
    if not instructor:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Instructor not found")
    for key, value in updated_instructor.dict(exclude_unset=True).items():
        setattr(instructor, key, value)
    db.commit()
    db.refresh(instructor)
    return instructor

def delete_instructor(instructor_id: int, db: Session):
    instructor = db.query(models.Instructor).filter(models.Instructor.id == instructor_id).first()
    if not instructor:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Instructor not found")
    db.delete(instructor)
    db.commit()
    return {"message": "Instructor deleted successfully"}