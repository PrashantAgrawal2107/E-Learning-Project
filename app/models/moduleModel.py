from sqlalchemy import Column, String, Integer, ForeignKey, Text
from sqlalchemy.orm import relationship
from .base import Base, IDMixin, TimestampMixin


class Module(Base, IDMixin, TimestampMixin):
    __tablename__ = "modules"

    name = Column(String(200), nullable=False)
    duration = Column(Integer, nullable=False)
    description = Column(Text, nullable=True)
    content_url = Column(Text, nullable=True)

    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    course = relationship("Course", back_populates="modules")

    quizzes = relationship("Quiz", back_populates="module", cascade="all, delete-orphan")