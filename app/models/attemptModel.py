from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base, IDMixin, TimestampMixin

class Attempt(Base, IDMixin, TimestampMixin):
    __tablename__ = "attempts"

    quiz_id = Column(Integer, ForeignKey("quizzes.id"), nullable=False)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    score = Column(Integer, nullable=False)

    quiz = relationship("Quiz", back_populates="attempts", passive_deletes=True)
    student = relationship("Student", back_populates="quiz_attempts", passive_deletes=True)

    answers = relationship(
        "AttemptAnswer",
        back_populates="attempt",
        cascade="all, delete-orphan"
    )
