from sqlalchemy import Column, Integer, ForeignKey, DateTime, CheckConstraint
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from .base import Base, IDMixin

class Enrollment(Base, IDMixin):
    __tablename__ = "enrollments"
     
    student_id = Column(Integer, ForeignKey("students.id", ondelete="CASCADE"), nullable=False)
    course_id = Column(Integer, ForeignKey("courses.id", ondelete="CASCADE"), nullable=False)
    enroll_date = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
     
    progress = Column(Integer, default=0, nullable=False)
    __table_args__ = (
        CheckConstraint("progress >= 0 AND progress <= 100", name="check_progress_range"),
    ) 
    student = relationship("Student", back_populates="enrollments", passive_deletes=True)
    course = relationship("Course", back_populates="enrollments", passive_deletes=True)