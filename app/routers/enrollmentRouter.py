from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..schemas import enrollmentSchema, courseSchema, studentSchema
from ..services import enrollmentServices as services
from ..core.dbConfig import get_db
from typing import List
from ..auth.authentication import require_role, get_current_user
from ..models.instructorModel import Instructor
from ..models.studentModel import Student

router = APIRouter(
    prefix="/enrollments",
    tags=["Enrollments"]
)

@router.post("/", response_model=enrollmentSchema.EnrollmentResponse, dependencies=[Depends(require_role("student", "instructor"))])
def create_enrollment(enrollment: enrollmentSchema.EnrollmentBase, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return services.create_enrollment(enrollment, db, current_user)

@router.get("/", response_model=List[enrollmentSchema.EnrollmentResponse])
def get_all_enrollments(db: Session = Depends(get_db)):
    return services.get_all_enrollments(db)

@router.get("/{enrollment_id}", response_model=enrollmentSchema.EnrollmentResponse)
def get_enrollment_by_id(enrollment_id: int, db: Session = Depends(get_db)):
    return services.get_enrollment_by_id(enrollment_id, db)

@router.put("/{enrollment_id}/update-progress", response_model=enrollmentSchema.EnrollmentResponse, dependencies=[Depends(require_role("student"))])
def update_progress(enrollment_id: int, enroll_update: enrollmentSchema.EnrollmentUpdate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return services.update_progress(enrollment_id, enroll_update, db, current_user)

@router.delete("/{enrollment_id}")
def delete_enrollment(enrollment_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return services.delete_enrollment(enrollment_id, db, current_user)

@router.get("/student/{student_id}/courses", response_model=List[courseSchema.CourseResponse])
def get_courses_by_student(student_id: int, db: Session = Depends(get_db)):
    return services.get_courses_by_student(student_id, db)

@router.get("/course/{course_id}/students", response_model=List[studentSchema.StudentResponse])
def get_students_by_course(course_id: int, db: Session = Depends(get_db)):
    return services.get_students_by_course(course_id, db)
