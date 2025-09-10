from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..core.dbConfig import get_db
from ..schemas import instructorSchema
from ..services import instructorServices
from ..auth.authentication import require_role, get_current_user
from ..models.instructorModel import Instructor
from ..schemas.sortSchema import SortSchema

router = APIRouter(prefix="/instructors", tags=["Instructors"])

@router.post("/", response_model=instructorSchema.InstructorResponse)
def create_instructor(instructor: instructorSchema.InstructorBase, db: Session = Depends(get_db)):
    return instructorServices.create_instructor(instructor, db)

@router.get("/", response_model=list[instructorSchema.InstructorResponse])
def get_all_instructors(
    db: Session = Depends(get_db),
    params: SortSchema = Depends()
):
    return instructorServices.get_all_instructors(db, params)

@router.get("/{instructor_id}", response_model=instructorSchema.InstructorResponse)
def get_instructor(instructor_id: int, db: Session = Depends(get_db)):
    instructor = instructorServices.get_instructor_by_id(instructor_id, db)
    if not instructor:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Instructor not found")
    return instructor

@router.put("/{instructor_id}", response_model=instructorSchema.InstructorResponse, dependencies=[Depends(require_role("instructor"))])
def update_instructor(instructor_id: int, updated_instructor: instructorSchema.InstructorUpdate, db: Session = Depends(get_db),current_user: Instructor = Depends(get_current_user)):
    return instructorServices.update_instructor(instructor_id, updated_instructor, db, current_user)

@router.delete("/{instructor_id}", dependencies=[Depends(require_role("instructor"))])
def delete_instructor(instructor_id: int, db: Session = Depends(get_db), current_user: Instructor = Depends(get_current_user)):
    return instructorServices.delete_instructor(instructor_id, db, current_user)