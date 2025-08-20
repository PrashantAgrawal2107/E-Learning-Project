from typing import List
from pydantic import BaseModel
from .studentSchema import StudentResponse
from .instructorSchema import InstructorResponse
from .courseSchema import CourseResponse

class SearchAllResponse(BaseModel):
    students: List[StudentResponse] = []
    instructors: List[InstructorResponse] = []
    courses: List[CourseResponse] = []
