from typing import Iterable, List

from api.models.api_group import ApiGroup, ApiGroupStudents, ApiGroupStats, ApiNewGroup
from api.models.managers.student_manager import StudentManager
from db.controllers.group_controller import GroupController
from db.models.groups import Group


class GroupManager:
    @staticmethod
    def get_api_group_from_group(group: Group) -> ApiGroup:
        return ApiGroup(id=group.group_id, name=group.name, students_count=len(group.students))

    @staticmethod
    def get_api_group_student_from_group(group: Group) -> ApiGroupStudents:
        api_group = ApiGroupStudents(
            **GroupManager.get_api_group_from_group(group).dict(),
            students=StudentManager.get_api_students_from_students(group.students.values())
        )
        return api_group

    @staticmethod
    def get_api_groups_students_from_groups(groups: Iterable[Group]) -> List[ApiGroup]:
        return [GroupManager.get_api_group_student_from_group(g) for g in groups]

    @staticmethod
    def get_api_group_stats_from_group(group: Group) -> ApiGroupStats:
        group_controller = GroupController(group)
        api_group_stats = ApiGroupStats(
            **GroupManager.get_api_group_from_group(group).dict(),
            grades_stats=group_controller.stats_by_subject,
            top_three_students=[
                StudentManager.get_api_student_avg_grade_from_student(student)
                for student in group_controller.top_three_students
            ]
        )
        return api_group_stats

    @staticmethod
    def get_group_from_group_new_api(group_new_api: ApiNewGroup) -> Group:
        return Group(name=group_new_api.name)
