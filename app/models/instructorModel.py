from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from .base import Base, IDMixin, TimestampMixin

class Instructor(Base, IDMixin, TimestampMixin):
    __tablename__ = "instructors"
    name = Column(String(100), nullable=False)
    email = Column(String(120), unique=True, nullable=False, index=True)
    password = Column(String(255), nullable=False)
    courses = relationship("Course", back_populates="instructor")