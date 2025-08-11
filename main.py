from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from dbConfig import get_db , engine
import models
import schemas

app = FastAPI()
models.Base.metadata.create_all(engine)


@app.get('/home')
def home():
    return 'Home Page'

@app.get('/about')
def about():
    return 'About Page'