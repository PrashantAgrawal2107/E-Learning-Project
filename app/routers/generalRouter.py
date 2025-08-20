from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..core.dbConfig import get_db
from ..services import instructorServices, studentServices
from ..auth.oauth2 import get_current_user

router = APIRouter(prefix="/general", tags=["General"])

@router.get("/")
def get_profile(db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    if current_user.role == 'instructor':
        return instructorServices.get_instructor_by_id(current_user.id , db)
    else:
        return studentServices.get_student_by_id(current_user.id, db)