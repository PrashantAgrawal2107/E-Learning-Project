from fastapi import FastAPI
from .core import dbConfig , config
from .routers import authentication , instructorRouter , studentRouter , courseRouter , moduleRouter, enrollmentRouter, quizRouter, attemptRouter, questionRouter
from sqlalchemy import create_engine
from app.models import Base

SQL_ALCHAMY_DATABASE_URL = config.settings.DATABASE_URL

app = FastAPI(title='E-Learning Platform')

engine = create_engine(
    SQL_ALCHAMY_DATABASE_URL
)
Base.metadata.create_all(engine)

# app.include_router(authentication.router)
app.include_router(instructorRouter.router)
app.include_router(studentRouter.router)
app.include_router(courseRouter.router)
app.include_router(moduleRouter.router)
app.include_router(enrollmentRouter.router)
app.include_router(quizRouter.router)
app.include_router(attemptRouter.router)
app.include_router(questionRouter.router)