from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..core.dbConfig import get_db
from ..schemas import studentSchema
from ..services import studentServices

router = APIRouter(prefix="/students", tags=["Students"])

@router.post("/", response_model=studentSchema.StudentResponse)
def create_student(student: studentSchema.StudentCreate, db: Session = Depends(get_db)):
    return studentServices.create_student(student, db)

@router.get("/", response_model=list[studentSchema.StudentResponse])
def get_all_students(db: Session = Depends(get_db)):
    return studentServices.get_all_students(db)

@router.get("/{student_id}", response_model=studentSchema.StudentResponse)
def get_student(student_id: int, db: Session = Depends(get_db)):
    student = studentServices.get_student_by_id(student_id, db)
    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")
    return student

@router.delete("/{student_id}")
def delete_student(student_id: int, db: Session = Depends(get_db)):
    return studentServices.delete_student(student_id, db)