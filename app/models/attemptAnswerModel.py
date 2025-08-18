from sqlalchemy import Column, Integer, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base, IDMixin

class AttemptAnswer(Base, IDMixin):
    __tablename__ = "attempt_answers"

    attempt_id = Column(Integer, ForeignKey("attempts.id", ondelete="CASCADE"), nullable=False)
    question_id = Column(Integer, ForeignKey("questions.id", ondelete="CASCADE"), nullable=False)
    selected_option_id = Column(Integer, ForeignKey("options.id", ondelete="CASCADE"), nullable=False)

    is_correct = Column(Boolean, default=False)

    attempt = relationship("Attempt", back_populates="answers", passive_deletes=True)
