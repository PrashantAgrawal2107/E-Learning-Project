from sqlalchemy import Column, String, Text, Integer, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base, IDMixin, TimestampMixin


class Quiz(Base, IDMixin, TimestampMixin):
    __tablename__ = "quizzes"

    name = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)

    # New relation -> every quiz belongs to a module
    module_id = Column(Integer, ForeignKey("modules.id"), nullable=False)
    module = relationship("Module", back_populates="quizzes")

    # existing relationships
    questions = relationship("Question", back_populates="quiz", cascade="all, delete-orphan")
    attempts = relationship("Attempt", back_populates="quiz", cascade="all, delete-orphan")
