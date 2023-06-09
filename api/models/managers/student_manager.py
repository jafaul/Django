from typing import Iterable, List

from api.models.api_student import ApiStudent, ApiStudentAvgGrade, ApiStudentGrades, ApiStudentStats, ApiNewStudent
from api.models.managers.grade_manager import GradeManager
from db.controllers.student_controller import StudentController
from db.models.students import Student


class StudentManager:

    @staticmethod
    def get_api_student_from_student(student: Student) -> ApiStudent:
        api_st = ApiStudent(
            id=student.student_id,
            first_name=student.first_name,
            last_name=student.last_name,
            birth_year=student.birth_year
        )
        return api_st

    @staticmethod
    def get_api_student_avg_grade_from_student(student: Student) -> ApiStudentAvgGrade:
        student_controller = StudentController(student)
        return ApiStudentAvgGrade(
            **StudentManager.get_api_student_from_student(student).dict(),
            avg_grade=student_controller.total_avg_grade
        )

    @staticmethod
    def get_api_student_grades_from_student(student: Student) -> ApiStudentGrades:
        api_st = ApiStudentGrades(
            **StudentManager.get_api_student_from_student(student).dict(),
            grades=GradeManager.get_api_grades_from_grades(list(student.grades.values())))
        return api_st

    @staticmethod
    def get_api_students_from_students(students: Iterable[Student]) -> List[ApiStudent]:
        return [StudentManager.get_api_student_from_student(st) for st in students]

    @staticmethod
    def get_api_student_stats_from_student(student: Student) -> ApiStudentStats:
        student_controller = StudentController(student)
        return ApiStudentStats(
            **StudentManager.get_api_student_grades_from_student(student).dict(),
            subjects=student_controller.stats_by_subjects,
            total_grades=student_controller.total_stat
        )

    @staticmethod
    def get_student_from_api_new_student(student_api: ApiNewStudent) -> Student:
        return Student(**student_api.dict())

