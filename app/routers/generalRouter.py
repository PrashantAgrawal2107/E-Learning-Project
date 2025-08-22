from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..core.dbConfig import get_db
from ..services import instructorServices, studentServices
from ..auth.authentication import get_current_user
from typing import Union
from ..schemas.studentSchema import StudentResponse
from ..schemas.instructorSchema import InstructorResponse

router = APIRouter(prefix="/general", tags=["General"])

@router.get("/profile", response_model=Union[StudentResponse , InstructorResponse])
def get_profile(db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    if current_user.role == 'instructor':
        return instructorServices.get_instructor_by_id(current_user.id , db)
    else:
        return studentServices.get_student_by_id(current_user.id, db)