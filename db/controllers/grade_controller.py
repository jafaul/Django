from db import database
from db.models.grades import Grade
from db.models.students import StudentIdType


class GradeController:
    def __init__(self, grade: Grade):
        self.grade = grade

    def save(self, student_id: StudentIdType):
        self.grade.grade_id, self.grade.date_grade = database.add_grade(self.grade)
        self.grade.student_id = student_id
