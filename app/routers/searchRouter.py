from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..core.dbConfig import get_db
from ..services import searchServices
from ..schemas import studentSchema, instructorSchema, courseSchema, searchSchema
from ..auth.authentication import get_current_user

router = APIRouter(prefix="/search", tags=["Search"])

@router.get("/students/{searchTerm}", response_model=list[studentSchema.StudentResponse])
def search_students(searchTerm: str, db: Session = Depends(get_db)):
    results = searchServices.search_students(db, searchTerm)
    return results

@router.get("/instructors/{searchTerm}", response_model=list[instructorSchema.InstructorResponse])
def search_instructors(searchTerm: str, db: Session = Depends(get_db)):
    results = searchServices.search_instructors(db, searchTerm)
    return results

@router.get("/courses/{searchTerm}", response_model=list[courseSchema.CourseResponse])
def search_courses(searchTerm: str, db: Session = Depends(get_db)):
    results = searchServices.search_courses(db, searchTerm)
    return results

@router.get("/all/{searchTerm}", response_model=searchSchema.SearchAllResponse)
def search_all(searchTerm: str, db: Session = Depends(get_db)):
    results = searchServices.search_all(db, searchTerm)
    return results

@router.get("/dashboard/{searchTerm}", response_model=searchSchema.SearchDashboardResponse)
def search_dashboard(searchTerm: str, 
                     db: Session = Depends(get_db), 
                     current_user = Depends(get_current_user)):
    results = searchServices.search_dashboard(db, searchTerm, current_user)
    return results
