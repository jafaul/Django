from typing import Union, List, Dict

from fastapi import APIRouter, HTTPException, Body
from starlette import status

from api.models.api_group import ApiGroup, ApiNewGroup, ApiGroupNewStudent, ApiNewGroupName
from api.models.managers.group_manager import GroupManager
from api.models.managers.student_manager import StudentManager
from api.routers.students import validation_student_id_exception
from db import database
from db.controllers.group_controller import GroupController
from db.database import read_all_data
from db.models.groups import Group

router = APIRouter(
    prefix="/groups",
    tags=["groups"]
)


def validation_group_id_exception(groups: Dict[int, Group],group_id: int):
    try:
        groups[group_id]
    except KeyError:
        raise HTTPException(status_code=404, detail="Group not found. Try to entry valid id")


@router.get("/", response_model=List[ApiGroup], status_code=status.HTTP_200_OK)
def read_groups():
    groups, _, _ = read_all_data()
    api_groups = GroupManager.get_api_groups_students_from_groups(groups.values())
    return api_groups


@router.get("/{group_id}", response_model=Union[dict, ApiGroup], status_code=status.HTTP_200_OK)
def get_group(group_id: int):
    groups, _, _ = read_all_data()
    validation_group_id_exception(groups, group_id)
    return GroupManager.get_api_group_student_from_group(groups[group_id])


@router.get("/{group_id}/stats", status_code=status.HTTP_200_OK)
def get_group_stats(group_id: int):
    groups, _, _ = read_all_data()
    validation_group_id_exception(groups, group_id)
    group = groups[group_id]
    students_in_group = group.students
    if len(group.students) == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Group #{group_id} has not any students yet."
        )
    amount_students_in_group = len(students_in_group)
    counter = 0
    for student in students_in_group.values():
        if len(student.grades) == 0:
            counter +=1
    if counter == amount_students_in_group:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Students in group #{group_id} have no grades yet. Check groups/{group_id}/"
        )

    return GroupManager.get_api_group_stats_from_group(group)


GROUP_EXAMPLE = {
    "name": "Group_name",
    "students": []
}


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_group(new_group_api: ApiNewGroup = Body(example=GROUP_EXAMPLE)):
    group = GroupManager.get_group_from_group_new_api(new_group_api)
    gc = GroupController(group)
    all_students = database.read_students()
    students_ids = new_group_api.students
    for student_id in students_ids:
        validation_student_id_exception(all_students, student_id)
    gc.save(students_ids)
    return GroupManager.get_api_group_student_from_group(group)


def validation_existing_student_in_group(student_id: int, group: Group):
    if group.students.get(student_id) is not None:
        raise HTTPException(
            status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
            detail=f"Student #{student_id} is already registered in the group. Check groups/{group.group_id}/"
        )


@router.post("/{group_id}/student", status_code=status.HTTP_201_CREATED)
def append_student_into_group(group_id: int, group_new_student: ApiGroupNewStudent):
    groups, students, _ = read_all_data()
    validation_group_id_exception(groups, group_id)
    group = groups[group_id]
    group_new_student_id = group_new_student.student_id
    validation_student_id_exception(students, group_new_student_id)
    validation_existing_student_in_group(group_new_student_id, group)
    gc = GroupController(group)
    gc.append_student(group_new_student_id)
    return GroupManager.get_api_group_student_from_group(group)


@router.get("/{group_id}/student/{student_id}")
def get_student_grades_from_group(group_id: int, student_id: int):
    groups, students, _ = read_all_data()
    validation_group_id_exception(groups, group_id)
    group = groups[group_id]
    validation_student_id_exception(students, student_id)
    validation_existing_student_in_group(student_id, group)
    student = group.students.get(student_id)
    return StudentManager.get_api_student_grades_from_student(student)


@router.post("/{group_id}/student/{student_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_student_from_group(group_id: int, student_id: int):
    groups, _, _ = read_all_data()
    validation_group_id_exception(groups, group_id)
    group = groups[group_id]
    validation_student_id_exception(group.students, student_id)
    gc = GroupController(group)
    gc.delete_student(student_id)
    return StudentManager.get_api_students_from_students(group.students.values())


@router.delete("/{group_id}/", status_code=status.HTTP_204_NO_CONTENT)
def delete_group(group_id: int):
    groups, _, _ = read_all_data()
    validation_group_id_exception(groups, group_id)
    group = groups[group_id]
    gc = GroupController(group)
    gc.delete()


@router.patch("/{group_id}")
def update_group_name(group_id: int, new_name: ApiNewGroupName):
    groups, _, _ = read_all_data()
    validation_group_id_exception(groups, group_id)
    group = groups[group_id]
    gc = GroupController(group)
    gc.update_group_name(new_name.name)
    return GroupManager.get_api_group_from_group(group)