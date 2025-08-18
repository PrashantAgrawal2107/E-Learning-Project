from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from .. import models, schemas


# Create a new module
def create_module(module: schemas.ModuleBase, db: Session):
    # Check if course exists (foreign key constraint safety)
    course = db.query(models.Course).filter(models.Course.id == module.course_id).first()
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Course with id {module.course_id} not found"
        )

    new_module = models.Module(
        name=module.name,
        duration=module.duration,
        description=module.description,
        content_url=module.content_url,
        course_id=module.course_id
    )
    db.add(new_module)
    db.commit()
    db.refresh(new_module)
    return new_module


# Get all modules
def get_all_modules(db: Session):
    modules = db.query(models.Module).all()
    return modules


# Get module by ID
def get_module_by_id(module_id: int, db: Session):
    module = db.query(models.Module).filter(models.Module.id == module_id).first()
    if not module:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Module with id {module_id} not found"
        )
    return module


# Update module
def update_module(module_id: int, updated_module: schemas.ModuleUpdate, db: Session):
    module = db.query(models.Module).filter(models.Module.id == module_id).first()
    if not module:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Module with id {module_id} not found"
        )

    update_data = updated_module.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(module, key, value)

    db.commit()
    db.refresh(module)
    return module


# Delete module
def delete_module(module_id: int, db: Session):
    module = db.query(models.Module).filter(models.Module.id == module_id).first()
    if not module:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Module with id {module_id} not found"
        )
    db.delete(module)
    db.commit()
    return {"message": f"Module with id {module_id} deleted successfully"}


# Get modules by Course ID (extra useful API)
def get_modules_by_course(course_id: int, db: Session):
    course = db.query(models.Course).filter(models.Course.id == course_id).first()
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Course with id {course_id} not found"
        )
    return course.modules
