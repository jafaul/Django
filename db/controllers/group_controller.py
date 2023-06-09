from collections import defaultdict
from statistics import median
from typing import List, Dict, Union, Callable

from db import database
from db.controllers.student_controller import StudentController, StatNameType
from db.models.grades import SubjectType
from db.models.groups import Group
from db.models.students import Student, StudentIdType


class GroupController:
    def __init__(self, group: Group):
        self.group = group
        self._students_controllers = []
        self._get_students_controllers()

    def _get_students_controllers(self) -> List[StudentController]:
        for student in self.group.students.values():
            student_controller = StudentController(student)
            self._students_controllers.append(student_controller)
        return self._students_controllers

    @staticmethod
    def _get_all_grades_by_subjects(group: Group) -> Dict[SubjectType, List[int]]:
        subjects_grades = {}
        group_controller = GroupController(group)
        for student_controller in group_controller._students_controllers:
            student_subjects_grades = student_controller.get_subjects_and_grades(student_controller.student)
            for subject, grades in student_subjects_grades.items():
                if subjects_grades.get(subject) is None:
                    subjects_grades[subject] = grades
                else:
                    subjects_grades[subject].extend(grades)
        return subjects_grades

    @staticmethod
    def _get_subjects_grades_stat(group: Group, stat_name: str, stat: Callable) -> Dict[SubjectType, Dict[StatNameType, Union[float, int]]]:
        subjects_and_grades = GroupController._get_all_grades_by_subjects(group)
        subjects_and_grades_stat = {}
        for subject, grades in subjects_and_grades.items():
            subjects_and_grades_stat[subject] = {stat_name: stat(grades)}
        return subjects_and_grades_stat

    @property
    def stats_by_subject(self) -> Dict[SubjectType, Dict[StatNameType, Union[float, int]]]:
        avg_grade = self._get_subjects_grades_stat(self.group, "avg", StudentController.avg)
        min_grade = self._get_subjects_grades_stat(self.group, "min", min)
        max_grade = self._get_subjects_grades_stat(self.group, "max", max)
        median_grade = self._get_subjects_grades_stat(self.group, "median", median)
        stats = defaultdict(dict)
        for row_stat in (avg_grade, min_grade, max_grade, median_grade):
            for subject, stat in row_stat.items():
                stats[subject].update(stat)
        return dict(stats)

    @property
    def top_three_students(self) -> List[Student]:
        sort_students_controller_by_avg_grade = sorted(
            self._students_controllers,
            key=lambda st_controller: st_controller.total_avg_grade,
            reverse=True
        )[:3]
        best_students = [student_controller.student for student_controller in sort_students_controller_by_avg_grade]
        return best_students

    def save(self, students_ids: List[StudentIdType]):
        group_id, students = database.add_group_with_relations(group=self.group, students_ids=students_ids)
        self.group.students = students
        self.group.group_id = group_id

    def append_student(self, student_id: int):
        self.group.students[student_id] = database.add_student_into_group_by_student_id(student_id, self.group.group_id)

    def delete(self):
        database.delete_all_group_data(self.group.group_id)

    def delete_student(self, student_id: int):
        database.delete_student_from_group(student_id, self.group.group_id)

    def update_group_name(self, new_name: str):
        self.group.name = new_name
        database.rewrite_group_name(self.group.group_id, self.group.name)
