# app/deps/auth.py
from typing import Optional
from fastapi import Depends, HTTPException, status
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from ..core.dbConfig import get_db
from ..core.security import oauth2_scheme, decode_token
from ..models.studentModel import Student
from ..models.instructorModel import Instructor

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# ---- Password utils ----
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

# ---- User retrieval/auth ----
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
    if not verify_password(password, user.password):
        return None
    return user

# ---- Dependencies for routes ----
def get_current_user(
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme),
):
    payload = decode_token(token)
    email: Optional[str] = payload.get("sub")
    role: Optional[str] = payload.get("role")

    if email is None or role is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # 🔑 role bhi bhejna hoga get_user_by_email me
    user = get_user_by_email(db, email, role)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user

def require_role(*allowed_roles: str):
    """
    Usage in route:
      current_user: Student = Depends(require_role("instructor"))
    OR apply at router level:
      dependencies=[Depends(require_role("instructor"))]
    """
    def _role_dependency(current_user: Student = Depends(get_current_user)) -> Student:
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions"
            )
        return current_user
    return _role_dependency
