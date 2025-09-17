from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..core.dbConfig import get_db
from ..schemas import studentSchema
from ..services import studentServices
from ..auth.authentication import require_role, get_current_user
from ..models.studentModel import Student
from ..schemas.sortSchema import SortSchema

router = APIRouter(prefix="/api/students", tags=["Students"])

@router.post("/", response_model=studentSchema.StudentResponse)
def create_student(student: studentSchema.StudentBase, db: Session = Depends(get_db)):
    return studentServices.create_student(student, db)

@router.get("/", response_model=list[studentSchema.StudentResponse])
def get_all_students(
    db: Session = Depends(get_db),
    params: SortSchema = Depends()            
):
    return studentServices.get_all_students(db, params)


@router.get("/{student_id}", response_model=studentSchema.StudentResponse)
def get_student(student_id: int, db: Session = Depends(get_db)):
    student = studentServices.get_student_by_id(student_id, db)
    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")
    return student

@router.put("/{student_id}", response_model=studentSchema.StudentResponse, dependencies=[Depends(require_role("student"))])
def update_student(student_id: int, updated_student: studentSchema.StudentUpdate, db: Session = Depends(get_db), current_user: Student = Depends(get_current_user)):
    return studentServices.update_student(student_id, updated_student, db, current_user)

@router.delete("/{student_id}", dependencies=[Depends(require_role("student"))])
def delete_student(student_id: int, db: Session = Depends(get_db), current_user: Student = Depends(get_current_user)):
    return studentServices.delete_student(student_id, db, current_user)