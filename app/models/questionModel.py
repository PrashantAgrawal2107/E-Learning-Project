from sqlalchemy import Column, Integer, Text, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base, IDMixin, TimestampMixin
class Question(Base, IDMixin, TimestampMixin):
    __tablename__ = "questions"
    content = Column(Text, nullable=False)
    quiz_id = Column(Integer, ForeignKey("quizzes.id"), nullable=False)
    quiz = relationship("Quiz", back_populates="questions")
    options = relationship("Option", back_populates="question")