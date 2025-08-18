from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..core.dbConfig import get_db
from .. import schemas
from ..services import courseServices as services
from ..auth.oauth2 import role_required

router = APIRouter(
    prefix="/courses",
    tags=["Courses"]
)

@router.post("/", response_model=schemas.CourseResponse)
def create_course(course: schemas.CourseBase, db: Session = Depends(get_db), current_user=Depends(role_required(["instructor"]))):
    return services.create_course(course, db)

@router.get("/", response_model=list[schemas.CourseResponse])
def get_courses(db: Session = Depends(get_db)):
    return services.get_all_courses(db)

@router.get("/{course_id}", response_model=schemas.CourseResponse)
def get_course(course_id: int, db: Session = Depends(get_db)):
    return services.get_course_by_id(course_id, db)

@router.put("/{course_id}", response_model=schemas.CourseResponse)
def update_course(course_id: int, updated_course: schemas.CourseUpdate, db: Session = Depends(get_db)):
    return services.update_course(course_id, updated_course, db)

@router.delete("/{course_id}")
def delete_course(course_id: int, db: Session = Depends(get_db)):
    return services.delete_course(course_id, db)









