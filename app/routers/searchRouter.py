from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..core.dbConfig import get_db
from ..services import searchServices

router = APIRouter(prefix="/search", tags=["Search"])

@router.get("/{searchTerm}")
def search_students(db: Session = Depends(get_db)):
    pass

@router.get("/{searchTerm}")
def search_instructors(db: Session = Depends(get_db)):
    pass

@router.get("/{searchTerm}")
def search_courses(db: Session = Depends(get_db)):
    pass

@router.get("/{searchTerm}")
def search_all(db: Session = Depends(get_db)):
    pass