from fastapi import APIRouter
from ..core import dbConfig
from sqlalchemy.orm import Session
from fastapi import APIRouter,Depends
from ..services import userServices
from ..schemas import userSchema

router = APIRouter(
    prefix="/user",
    tags=['Users']
)

get_db = dbConfig.get_db


@router.post('/', response_model=userSchema.ShowUser)
def create_user(request: userSchema.User,db: Session = Depends(get_db)):
    return userServices.create(request,db)

@router.get('/{id}',response_model=userSchema.ShowUser)
def get_user(id:int,db: Session = Depends(get_db)):
    return userServices.show(id,db)