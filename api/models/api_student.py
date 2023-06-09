from typing import List, Dict, Any

from pydantic import BaseModel

from api.models.api_grades import ApiGrade
from db.controllers.student_controller import StatNameType
from db.models.grades import SubjectType


class ApiNewStudent(BaseModel):
    first_name: str
    last_name: str
    birth_year: int


class ApiStudent(BaseModel):
    id: int
    first_name: str
    last_name: str
    birth_year: int


class ApiStudentAvgGrade(ApiStudent):
    avg_grade: float


class ApiStudentGrades(ApiStudent):
    grades: List[ApiGrade]


class ApiStudentStats(ApiStudent):
    subjects: Dict[SubjectType, Dict[StatNameType, Any]]
    total_grades: Dict[StatNameType, Any]


