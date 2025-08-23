from typing import List
from pydantic import BaseModel
from .studentSchema import StudentResponse
from .instructorSchema import InstructorResponse
from .courseSchema import CourseResponse
from .moduleSchema import ModuleResponse
from .quizSchema import QuizResponse

class SearchAllResponse(BaseModel):
    students: List[StudentResponse] = []
    instructors: List[InstructorResponse] = []
    courses: List[CourseResponse] = []

class SearchDashboardResponse(BaseModel):
    courses: List[CourseResponse] = []
    modules: List[ModuleResponse] = []
    quizzes: List[QuizResponse] = []

    class Config:
        from_attributes = True