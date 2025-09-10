from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, DateTime, func

Base = declarative_base()


class IDMixin:
    id = Column(Integer, primary_key=True, autoincrement=True)
    

class TimestampMixin:
    created_on = Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now()  
    )
    updated_on = Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now()  
    )