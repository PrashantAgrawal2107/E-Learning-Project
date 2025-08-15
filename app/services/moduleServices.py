from sqlalchemy.orm import Session
from .. import models, schemas
from fastapi import HTTPException, status

def create_module(module: schemas.ModuleBase, db: Session):
    # Validate instructor exists
    instructor = db.query(models.Instructor).filter(models.Instructor.id == module.instructor_id).first()
    if not instructor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Instructor with id {module.instructor_id} does not exist"
        )
    db_module = models.Module(**module.model_dump())
    db.add(db_module)
    db.commit()
    db.refresh(db_module)
    return db_module

def get_all_modules(db: Session):
    return db.query(models.Module).all()

def get_module_by_id(module_id: int, db: Session):
    module = db.query(models.Module).filter(models.Module.id == module_id).first()
    if not module:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="module not found"
        )
    return module

def update_module(module_id: int, updated_module: schemas.ModuleUpdate, db: Session):
    module = db.query(models.Module).filter(models.Module.id == module_id).first()
    if not module:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="module not found"
        )
    for key, value in updated_module.model_dump(exclude_unset=True).items():
        setattr(module, key, value)
    db.commit()
    db.refresh(module)
    return module

def delete_module(module_id: int, db: Session):
    module = db.query(models.Module).filter(models.Module.id == module_id).first()
    if not module:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="module not found"
        )
    db.delete(module)
    db.commit()
    return {"message": "module deleted successfully"}