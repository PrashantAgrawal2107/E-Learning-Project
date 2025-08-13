from sqlalchemy import Column, String, Text
from sqlalchemy.orm import relationship
from .base import Base, IDMixin, TimestampMixin
class Quiz(Base, IDMixin, TimestampMixin):
    __tablename__ = "quizzes"
    name = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    questions = relationship("Question", back_populates="quiz")
    attempts = relationship("Attempt", back_populates="quiz")
    assigned_courses = relationship("QuizAssign", back_populates="quiz")