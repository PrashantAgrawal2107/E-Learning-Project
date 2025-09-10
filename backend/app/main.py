from fastapi import FastAPI
from .core import config
from .routers import authRouter , instructorRouter , studentRouter , courseRouter , moduleRouter, enrollmentRouter, quizRouter, attemptRouter, questionRouter, generalRouter, searchRouter
from sqlalchemy import create_engine
from app.models import Base
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

SQL_ALCHAMY_DATABASE_URL = config.settings.DATABASE_URL

app = FastAPI(title='E-Learning Platform')

origins = [
    "http://localhost",
    "http://localhost:5173", # The default port for Vite
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

engine = create_engine(
    SQL_ALCHAMY_DATABASE_URL
)
Base.metadata.create_all(engine)

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(authRouter.router)
app.include_router(generalRouter.router)
app.include_router(searchRouter.router)
app.include_router(instructorRouter.router)
app.include_router(studentRouter.router)
app.include_router(courseRouter.router)
app.include_router(moduleRouter.router)
app.include_router(enrollmentRouter.router)
app.include_router(quizRouter.router)
app.include_router(attemptRouter.router)
app.include_router(questionRouter.router)