from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session

from ..core.dbConfig import get_db
from ..auth.security import create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
from ..auth.authentication import authenticate_user
from ..schemas.authSchema import LoginRequest, UserResponse

router = APIRouter(prefix="/api/auth", tags=["Auth"])

@router.post("/login", response_model=UserResponse)
def login(
    payload: LoginRequest,
    db: Session = Depends(get_db),
    response: Response = None
):
    user = authenticate_user(db, payload.email, payload.password, payload.role) 
    print(user) 
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials or role"
        )

    access_token = create_access_token(
        data={"sub": user.email, "role": user.role}, 
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    
    response.set_cookie(
        key="access_token", 
        value=access_token,
        httponly=True,
        max_age=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    )
    
    return {"id": user.id, "name": user.name, "role": user.role, "email": user.email, "created_on": user.created_on, "updated_on": user.updated_on}

@router.post("/signout")
def signout(response: Response):
    response.delete_cookie(key="access_token", httponly=True)
    return {"message": "User signed out successfully"}
