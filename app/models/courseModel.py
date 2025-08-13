from sqlalchemy import Column, String, Integer, ForeignKey, Text
from sqlalchemy.orm import relationship
from .base import Base, IDMixin, TimestampMixin

class Course(Base, IDMixin, TimestampMixin):
    __tablename__ = "courses"
    coursename = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    duration = Column(Integer, nullable=False)  # in hours
    instructor_id = Column(Integer, ForeignKey("instructors.id"), nullable=False)
    instructor = relationship("Instructor", back_populates="courses")
    modules = relationship("Module", back_populates="course")
    enrollments = relationship("Enrollment", back_populates="course")
    assigned_quizzes = relationship("QuizAssign", back_populates="course")