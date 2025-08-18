from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from ..core import dbConfig
from ..auth.hashing import Hash
from ..auth import token
from sqlalchemy.orm import Session
from ..models import studentModel , instructorModel

router = APIRouter(tags=['Authentication'])

@router.post('/studentLogin')
def login(request:OAuth2PasswordRequestForm = Depends(), db: Session = Depends(dbConfig.get_db)):
    student = db.query(studentModel.Student).filter(studentModel.Student.email == request.username).first()
    
    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Invalid Credentials")
    if not Hash.verify(student.password, request.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Incorrect password")

    access_token = token.create_access_token(data={"sub": student.email , "role": student.role})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post('/instructorLogin')
def login(request:OAuth2PasswordRequestForm = Depends(), db: Session = Depends(dbConfig.get_db)):
    instructor = db.query(instructorModel.Instructor).filter(instructorModel.Instructor.email == request.username).first()
    
    if not instructor:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Invalid Credentials")
    if not Hash.verify(instructor.password, request.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Incorrect password")

    access_token = token.create_access_token(data={"sub": instructor.email , "role": instructor.role})
    return {"access_token": access_token, "token_type": "bearer"}