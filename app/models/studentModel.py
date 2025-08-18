from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from .base import Base, IDMixin, TimestampMixin

class Student(Base, IDMixin, TimestampMixin):
    __tablename__ = "students"

    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False, index=True)
    password = Column(String(300), nullable=False)
    role = Column(String , default='student')

    enrollments = relationship(
        "Enrollment",
        back_populates="student",
        cascade="all, delete-orphan"
    )

    quiz_attempts = relationship(
        "Attempt",
        back_populates="student",
        cascade="all, delete-orphan"
    )
