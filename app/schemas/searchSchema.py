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
    courses: list[CourseResponse]
    modules: list[ModuleResponse]
    quizzes: list[QuizResponse]

    class Config:
        orm_mode = True