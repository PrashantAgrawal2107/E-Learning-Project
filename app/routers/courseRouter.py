from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..core.dbConfig import get_db
from .. import schemas
from ..services import courseServices as services
from ..auth.oauth2 import require_role, get_current_user
from ..models.instructorModel import Instructor

router = APIRouter(
    prefix="/courses",
    tags=["Courses"]
)

@router.post("/", response_model=schemas.CourseResponse , dependencies=[Depends(require_role("instructor"))])
def create_course(course: schemas.CourseBase, db: Session = Depends(get_db), current_user: Instructor = Depends(get_current_user)):
    return services.create_course(course, db, current_user)

@router.get("/", response_model=list[schemas.CourseResponse])
def get_courses(db: Session = Depends(get_db)):
    return services.get_all_courses(db)

@router.get("/{course_id}", response_model=schemas.CourseResponse)
def get_course(course_id: int, db: Session = Depends(get_db)):
    return services.get_course_by_id(course_id, db)

@router.put("/{course_id}", response_model=schemas.CourseResponse, dependencies=[Depends(require_role("instructor"))])
def update_course(course_id: int, updated_course: schemas.CourseUpdate, db: Session = Depends(get_db), current_user: Instructor = Depends(get_current_user)):
    return services.update_course(course_id, updated_course, db, current_user)

@router.delete("/{course_id}" , dependencies=[Depends(require_role("instructor"))])
def delete_course(course_id: int, db: Session = Depends(get_db), current_user: Instructor = Depends(get_current_user)):
    return services.delete_course(course_id, db, current_user)
