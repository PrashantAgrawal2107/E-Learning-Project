from sqlalchemy import Column, Integer, Text, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base, IDMixin

class Option(Base, IDMixin):
    __tablename__ = "options"

    description = Column(Text, nullable=False)
    is_correct = Column(Boolean, default=False)

    question_id = Column(
        Integer,
        ForeignKey("questions.id", ondelete="CASCADE"),
        nullable=False
    )

    question = relationship(
        "Question",
        back_populates="options",
        passive_deletes=True
    )
