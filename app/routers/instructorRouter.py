from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..core.dbConfig import get_db
from ..schemas import instructorSchema
from ..services import instructorServices

router = APIRouter(prefix="/instructors", tags=["Instructors"])

@router.post("/", response_model=instructorSchema.InstructorOut)
def create_instructor(instructor: instructorSchema.InstructorCreate, db: Session = Depends(get_db)):
    return instructorServices.create_instructor(instructor, db)

@router.get("/", response_model=list[instructorSchema.InstructorOut])
def get_all_instructors(db: Session = Depends(get_db)):
    return instructorServices.get_all_instructors(db)

@router.get("/{instructor_id}", response_model=instructorSchema.InstructorOut)
def get_instructor(instructor_id: int, db: Session = Depends(get_db)):
    instructor = instructorServices.get_instructor_by_id(instructor_id, db)
    if not instructor:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Instructor not found")
    return instructor

@router.delete("/{instructor_id}")
def delete_instructor(instructor_id: int, db: Session = Depends(get_db)):
    return instructorServices.delete_instructor(instructor_id, db)