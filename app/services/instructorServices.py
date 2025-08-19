from sqlalchemy.orm import Session
from .. import models, schemas
from fastapi import HTTPException, status
from ..auth.hashing import Hash
from ..models.instructorModel import Instructor

def create_instructor(instructor: schemas.InstructorBase, db: Session):
    
    existing_instructor = db.query(models.Instructor).filter(models.Instructor.email == instructor.email).first()
    if existing_instructor:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
   
    hashed_password = Hash.bcrypt(instructor.password)

    
    db_instructor = models.Instructor(
        name=instructor.name,
        email=instructor.email,
        password=hashed_password
    )

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

def update_instructor(instructor_id: int, updated_instructor: schemas.InstructorUpdate, db: Session, current_user: Instructor):
    instructor = db.query(models.Instructor).filter(models.Instructor.id == instructor_id).first()
    if not instructor:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Instructor not found")
    
    if instructor.id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to update this instrutor's profile"
        )
    
    existing_instructor = db.query(models.Instructor).filter(models.Instructor.email == updated_instructor.email).first()
    if existing_instructor:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    update_data = updated_instructor.model_dump(exclude_unset=True)
    if "password" in update_data:
        update_data["password"] = Hash.bcrypt(update_data["password"])

    # Update updated_at timestamp
    # update_data["updated_on"] = datetime.utcnow()

    for key, value in update_data.items():
        setattr(instructor, key, value)

    db.commit()
    db.refresh(instructor)
    return instructor

def delete_instructor(instructor_id: int, db: Session, current_user: Instructor):
    instructor = db.query(models.Instructor).filter(models.Instructor.id == instructor_id).first()
    if not instructor:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Instructor not found")
    
    if instructor.id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to delete this instrutor's profile"
        )
    
    db.delete(instructor)
    db.commit()
    return {"message": "Instructor deleted successfully"}