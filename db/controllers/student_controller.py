from collections import defaultdict
from statistics import median
from typing import Dict, Union, Callable, List

from db import database
from db.models.grades import SubjectType
from db.models.students import Student

StatNameType = str


class StudentController:
    def __init__(self, student: Student):
        self.student = student

    @staticmethod
    def get_subjects_and_grades(student: Student) -> Dict[SubjectType, List[int]]:
        subjects_and_grades = {}
        for grade in student.grades.values():
            if grade.subject not in subjects_and_grades:
                subjects_and_grades[grade.subject] = [grade.grade]
            else:
                subjects_and_grades[grade.subject].append(grade.grade)
        return subjects_and_grades

    @staticmethod
    def _get_all_grades(student: Student) -> List[int]:
        return list(map(lambda g: g.grade, student.grades.values()))

    @property
    def total_avg_grade(self) -> float:
        all_grades = StudentController._get_all_grades(self.student)
        return sum(all_grades) / len(all_grades)

    @property
    def total_count_grades(self) -> int:
        return len(self.student.grades)

    @property
    def total_min_grade(self) -> int:
        return min(StudentController._get_all_grades(self.student))

    @property
    def total_max_grade(self) -> int:
        return max(StudentController._get_all_grades(self.student))

    @property
    def total_median_grade(self) -> Union[int, float]:
        return median(StudentController._get_all_grades(self.student))

    @property
    def total_stat(self) -> Dict[StatNameType, Union[int, float]]:
        total_stats = {
            "grades_count": self.total_count_grades,
            "avg": self.total_avg_grade,
            "min": self.total_min_grade,
            "max": self.total_max_grade,
            "median": self.total_median_grade
        }
        return total_stats

    @staticmethod
    def _get_subjects_grades_stat(
            student: Student, stat_name: StatNameType, stat: Callable
    ) -> Dict[SubjectType, Dict[StatNameType, Union[float, int]]]:
        subjects_and_grades = StudentController.get_subjects_and_grades(student)
        subjects_and_grades_stat = {}
        for subject, grades in subjects_and_grades.items():
            subjects_and_grades_stat[subject] = {stat_name: stat(grades)}
        return subjects_and_grades_stat

    @staticmethod
    def _get_subjects_grades_count(student: Student) -> Dict[SubjectType, Dict[StatNameType, int]]:
        return StudentController._get_subjects_grades_stat(student, "grades_count", len)

    @staticmethod
    def avg(grades: List[int]) -> float:
        return sum(grades) / len(grades)

    @staticmethod
    def _get_avg_grade_by_subject(student: Student) -> Dict[SubjectType, Dict[StatNameType, float]]:
        return StudentController._get_subjects_grades_stat(student, "avg", StudentController.avg)

    @staticmethod
    def _get_grade_min_by_subject(student: Student) -> Dict[SubjectType, Dict[StatNameType, int]]:
        return StudentController._get_subjects_grades_stat(student, "min", min)

    @staticmethod
    def _get_grade_max_by_subject(student: Student) -> Dict[SubjectType, Dict[StatNameType, int]]:
        return StudentController._get_subjects_grades_stat(student, "max", max)

    @staticmethod
    def _get_grade_median_by_subject(student: Student) -> Dict[SubjectType, Dict[StatNameType, Union[str, float]]]:
        return StudentController._get_subjects_grades_stat(student, "median", median)

    @property
    def stats_by_subjects(self) -> Dict[SubjectType, Dict[StatNameType, Union[int, float]]]:
        stat_count = StudentController._get_subjects_grades_count(self.student)
        stat_avg = StudentController._get_avg_grade_by_subject(self.student)
        stat_min = StudentController._get_grade_min_by_subject(self.student)
        stat_max = StudentController._get_grade_max_by_subject(self.student)
        stat_median = StudentController._get_grade_median_by_subject(self.student)
        stats_of_student = defaultdict(dict)
        for row_stat in (stat_count, stat_avg, stat_min, stat_max, stat_median):
            for subject, stat in row_stat.items():
                stats_of_student[subject].update(stat)
        return dict(stats_of_student)

    def save(self):
        student_id = database.add_student(self.student)
        self.student.student_id = student_id

    def delete(self):
        database.delete_all_student_data(self.student.student_id)


