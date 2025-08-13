from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base, IDMixin

class QuizAssign(Base, IDMixin):
    __tablename__ = "quiz_assign"
    quiz_id = Column(Integer, ForeignKey("quizzes.id"), nullable=False)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=True)
    module_id = Column(Integer, ForeignKey("modules.id"), nullable=True)
    quiz = relationship("Quiz", back_populates="assigned_courses")
    course = relationship("Course", back_populates="assigned_quizzes")
    module = relationship("Module", back_populates="assigned_quizzes")
