from sqlalchemy import Column, String, Integer, ForeignKey, Text
from sqlalchemy.orm import relationship
from .base import Base, IDMixin, TimestampMixin

class Course(Base, IDMixin, TimestampMixin):
    __tablename__ = "courses"

    name = Column(String(200), nullable=False)   # consistent naam
    description = Column(Text, nullable=True)
    duration = Column(Integer, nullable=False)   # in hours

    instructor_id = Column(
        Integer,
        ForeignKey("instructors.id", ondelete="CASCADE"),
        nullable=False,
    )

    instructor = relationship(
        "Instructor",
        back_populates="courses",
        passive_deletes=True
    )

    modules = relationship(
        "Module",
        back_populates="course",
        cascade="all, delete-orphan",
        passive_deletes=True
    )

    enrollments = relationship(
        "Enrollment",
        back_populates="course",
        cascade="all, delete-orphan",
        passive_deletes=True
    )
