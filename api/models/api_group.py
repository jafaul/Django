from typing import List, Dict, Any

from pydantic import BaseModel

from api.models.api_student import ApiStudent
from db.controllers.student_controller import StatNameType
from db.models.grades import SubjectType
from db.models.students import StudentIdType


class ApiGroup(BaseModel):
    id: int
    name: str
    students_count: int


class ApiNewGroupName(BaseModel):
    name: str


class ApiGroupStudents(ApiGroup):
    students: List[ApiStudent]


class ApiGroupNewStudent(BaseModel):
    student_id: int


class ApiNewGroup(BaseModel):
    name: str
    students: List[StudentIdType]


class ApiGroupStats(ApiGroup):
    grades_stats: Dict[SubjectType, Dict[StatNameType, Any]]
    top_three_students: List[ApiStudent]
