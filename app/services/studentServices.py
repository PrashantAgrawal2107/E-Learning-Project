from sqlalchemy.orm import Session
from .. import models, schemas
from fastapi import HTTPException, status
from ..auth.hashing import Hash
from datetime import datetime
from ..models.studentModel import Student
from ..auth.validations import sort_validation

def create_student(student: schemas.StudentBase, db: Session):
    
    existing_student = db.query(models.Student).filter(models.Student.email == student.email).first()
    if existing_student:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
   
    hashed_password = Hash.bcrypt(student.password)

    db_student = models.Student(
        name=student.name,
        email=student.email,
        password=hashed_password
    )

    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student

def get_all_students(db: Session, params):

    valid_sort_fields = {
        "name": Student.name,
        "created_on": Student.created_on,
        "updated_on": Student.updated_on
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

    students = (
        db.query(Student)
        .order_by(sort)
        .offset(skip*limit)   
        .limit(limit)   
        .all()
    )

    return students


def get_student_by_id(student_id: int, db: Session):
    student = db.query(models.Student).filter(models.Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")
    return student

def update_student(student_id: int, updated_student: schemas.StudentUpdate, db: Session, current_user : Student):
    student = db.query(models.Student).filter(models.Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")
    
    if student.id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to update this student's profile"
        )
    
    
    existing_student = db.query(models.Student).filter(models.Student.email == updated_student.email).first()
    if existing_student:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
  
    update_data = updated_student.model_dump(exclude_unset=True)
    if "password" in update_data:
        update_data["password"] = Hash.bcrypt(update_data["password"])

    # Update updated_at timestamp
    # update_data["updated_on"] = datetime.utcnow()

    for key, value in update_data.items():
        setattr(student, key, value)

    db.commit()
    db.refresh(student)
    return student

def delete_student(student_id: int, db: Session, current_user: Student):
    student = db.query(models.Student).filter(models.Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")
    
    if student.id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to delete this student's profile"
        )
    
    db.delete(student)
    db.commit()
    return {"message": "Student deleted successfully"}