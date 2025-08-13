from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from .base import Base, IDMixin
class Enrollment(Base, IDMixin):
    __tablename__ = "enrollments"
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    enroll_date = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    student = relationship("Student", back_populates="enrollments")
    course = relationship("Course", back_populates="enrollments")