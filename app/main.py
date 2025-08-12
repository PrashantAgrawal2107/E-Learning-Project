from fastapi import FastAPI
from .core import dbConfig , config
from .routers import userRouter , authentication
from sqlalchemy import create_engine
from app.models import Base

SQL_ALCHAMY_DATABASE_URL = config.settings.DATABASE_URL

app = FastAPI(title='E-Learning Platform')

engine = create_engine(
    SQL_ALCHAMY_DATABASE_URL
)
Base.metadata.create_all(engine)

app.include_router(userRouter.router)
app.include_router(authentication.router)