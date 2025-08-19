from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..core.dbConfig import get_db
from .. import schemas
from ..services import moduleServices as services
from ..auth.oauth2 import require_role, get_current_user
from ..models.instructorModel import Instructor

router = APIRouter(
    prefix="/modules",
    tags=["Modules"]
)

@router.post("/", response_model=schemas.ModuleResponse, dependencies=[Depends(require_role("instructor"))])
def create_module(Module: schemas.ModuleBase, db: Session = Depends(get_db), current_user: Instructor = Depends(get_current_user)):
    return services.create_module(Module, db, current_user)

@router.get("/", response_model=list[schemas.ModuleResponse])
def get_modules(db: Session = Depends(get_db)):
    return services.get_all_modules(db)

@router.get("/{module_id}", response_model=schemas.ModuleResponse)
def get_module(module_id: int, db: Session = Depends(get_db)):
    return services.get_module_by_id(module_id, db)

@router.put("/{module_id}", response_model=schemas.ModuleResponse, dependencies=[Depends(require_role("instructor"))])
def update_module(module_id: int, updated_module: schemas.ModuleUpdate, db: Session = Depends(get_db), current_user: Instructor = Depends(get_current_user)):
    return services.update_module(module_id, updated_module, db, current_user)

@router.delete("/{module_id}", dependencies=[Depends(require_role("instructor"))])
def delete_module(module_id: int, db: Session = Depends(get_db), current_user: Instructor = Depends(get_current_user)):
    return services.delete_module(module_id, db, current_user)

@router.get("/course/{course_id}", response_model=list[schemas.ModuleResponse])
def get_modules_by_course(course_id: int, db: Session = Depends(get_db)):
    return services.get_modules_by_course(course_id, db)