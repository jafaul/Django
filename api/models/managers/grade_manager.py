from datetime import datetime
from typing import List

from api.models.api_grades import ApiGrade, ApiNewGrade
from db.models.grades import Grade


class GradeManager:
    @staticmethod
    def get_api_grade_from_grade(gr: Grade) -> ApiGrade:
        return ApiGrade(
            id=gr.grade_id,
            subject=gr.subject,
            grade=gr.grade,
            date=datetime.strptime(str(gr.date_grade), '%Y-%m-%d').strftime('%d.%m.%Y')
        )

    @staticmethod
    def get_api_grades_from_grades(grades: List[Grade]) -> List[ApiGrade]:
        return [GradeManager.get_api_grade_from_grade(gr) for gr in grades]

    @staticmethod
    def get_grade_from_api_new_grade(api_grade: ApiNewGrade) -> Grade:
        return Grade(subject=api_grade.subject, grade=api_grade.grade)

