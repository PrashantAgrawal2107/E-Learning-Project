from typing import Optional
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..core.dbConfig import get_db
from .security import decode_token , get_token
from ..models.studentModel import Student
from ..models.instructorModel import Instructor
from .hashing import Hash

def get_user_by_email(db: Session, email: str, role: str):
    if role == "student":
        return db.query(Student).filter(Student.email == email).first()
    elif role == "instructor":
        return db.query(Instructor).filter(Instructor.email == email).first()
    return None

def authenticate_user(db: Session, email: str, password: str, role: str):
    user = get_user_by_email(db, email, role)
    if not user:
        return None
    if not Hash.verify(user.password, password):
        return None
    return user

def get_current_user(
    db: Session = Depends(get_db),
    token: str = Depends(get_token),
):
    print(token)
    payload = decode_token(token)
    email: Optional[str] = payload.get("sub")
    role: Optional[str] = payload.get("role")

    if email is None or role is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    print(email)
    print(role)
    user = get_user_by_email(db, email, role)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user

def require_role(*allowed_roles: str):
    def _role_dependency(current_user = Depends(get_current_user)):
        print(current_user)
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions"
            )
        return current_user
    return _role_dependency
