from sqlalchemy.orm import Session
from ..models import userModel
from fastapi import HTTPException,status
from ..auth.hashing import Hash
from ..schemas import userSchema

def create(request: userSchema.User,db:Session):
    new_user = userModel.User(name=request.name,email=request.email,password=Hash.bcrypt(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def show(id:int,db:Session):
    user = db.query(userModel.User).filter(userModel.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with the id {id} is not available")
    return user