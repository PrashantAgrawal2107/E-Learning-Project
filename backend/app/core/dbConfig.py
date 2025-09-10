from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

SQL_ALCHAMY_DATABASE_URL = settings.DATABASE_URL

engine = create_engine(
    SQL_ALCHAMY_DATABASE_URL
)

SessionLocal = sessionmaker(bind = engine , autocommit = False , autoflush = False)

def get_db():
    db = SessionLocal()

    try: 
        yield db
    finally:
        db.close()
