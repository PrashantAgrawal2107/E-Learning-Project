from fastapi import HTTPException, status, UploadFile
from sqlalchemy.orm import Session
from .. import models, schemas
from ..models.instructorModel import Instructor
from ..models.moduleModel import Module
import os


UPLOAD_DIR = "static/uploads"

# Ensure upload folder exists
os.makedirs(UPLOAD_DIR, exist_ok=True)


def create_module(module: schemas.ModuleBase, db: Session, current_user: Instructor):
    
    course = db.query(models.Course).filter(models.Course.id == module.course_id).first()
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Course with id {module.course_id} not found"
        )
    
    if course.instructor_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to create modules for this course"
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


def get_all_modules(db: Session):
    modules = db.query(models.Module).all()
    return modules


def get_module_by_id(module_id: int, db: Session):
    module = db.query(models.Module).filter(models.Module.id == module_id).first()
    if not module:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Module with id {module_id} not found"
        )
    return module


def update_module(module_id: int, updated_module: schemas.ModuleUpdate, db: Session, current_user: Instructor):
    module = db.query(models.Module).filter(models.Module.id == module_id).first()
    if not module:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Module with id {module_id} not found"
        )
    
    if module.course.instructor_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to update this module"
        )

    update_data = updated_module.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(module, key, value)

    db.commit()
    db.refresh(module)
    return module


def delete_module(module_id: int, db: Session, current_user: Instructor):
    module = db.query(models.Module).filter(models.Module.id == module_id).first()
    if not module:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Module with id {module_id} not found"
        )
    
    if module.course.instructor_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to delete this module"
        )

    db.delete(module)
    db.commit()
    return {"message": f"Module with id {module_id} deleted successfully"}


def get_modules_by_course(course_id: int, db: Session):
    course = db.query(models.Course).filter(models.Course.id == course_id).first()
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Course with id {course_id} not found"
        )
    return course.modules

def save_module_file(db: Session, module_id: int, file: UploadFile, current_user: Instructor):
    print(f"Uploading file for module {module_id} by user {current_user.id}")
    module = db.query(Module).filter(Module.id == module_id).first()
    if not module:
        raise HTTPException(status_code=404, detail=f"Module with id {module_id} not found")
    
    if module.course.instructor_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to upload file in this module"
        )

    file_location = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_location, "wb") as f:
        f.write(file.file.read())

    file_url = f"/{file_location}"

    if not module.contents:
        module.contents = []
    if isinstance(module.contents, str):
        module.contents = [module.contents]

    module.contents.append(file_url)

    db.add(module)
    db.commit()
    db.refresh(module)

    return {"message": "File uploaded successfully", "file_url": file_url}
