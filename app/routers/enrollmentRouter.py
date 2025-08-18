from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..schemas import enrollmentSchema, courseSchema, studentSchema
from ..services import enrollmentServices as services
from ..core.dbConfig import get_db
from typing import List

router = APIRouter(
    prefix="/enrollments",
    tags=["Enrollments"]
)

# ---------------- CREATE ----------------
@router.post("/", response_model=enrollmentSchema.EnrollmentBase)
def create_enrollment(enrollment: enrollmentSchema.EnrollmentBase, db: Session = Depends(get_db)):
    return services.create_enrollment(enrollment, db)

# ---------------- GET ALL ----------------
@router.get("/", response_model=List[enrollmentSchema.EnrollmentBase])
def get_all_enrollments(db: Session = Depends(get_db)):
    return services.get_all_enrollments(db)

# ---------------- GET BY ID ----------------
@router.get("/{enrollment_id}", response_model=enrollmentSchema.EnrollmentBase)
def get_enrollment_by_id(enrollment_id: int, db: Session = Depends(get_db)):
    return services.get_enrollment_by_id(enrollment_id, db)

# ---------------- DELETE ----------------
@router.delete("/{enrollment_id}")
def delete_enrollment(enrollment_id: int, db: Session = Depends(get_db)):
    return services.delete_enrollment(enrollment_id, db)

# ---------------- NEW: Get all courses by student ----------------
@router.get("/student/{student_id}/courses", response_model=List[courseSchema.CourseResponse])
def get_courses_by_student(student_id: int, db: Session = Depends(get_db)):
    return services.get_courses_by_student(student_id, db)

# ---------------- NEW: Get all students by course ----------------
@router.get("/course/{course_id}/students", response_model=List[studentSchema.StudentResponse])
def get_students_by_course(course_id: int, db: Session = Depends(get_db)):
    return services.get_students_by_course(course_id, db)
