from typing import Union,  Dict

from fastapi import APIRouter, HTTPException, Body
from starlette import status

from api.models.api_grades import ApiNewGrade
from api.models.api_student import ApiStudent, ApiNewStudent
from api.models.managers.grade_manager import GradeManager
from api.models.managers.student_manager import StudentManager
from db.controllers.grade_controller import GradeController
from db.controllers.student_controller import StudentController
from db.database import read_all_data
from db.models.students import Student


router = APIRouter(
    prefix="/students",
    tags=["students"]
)


STUDENT_EXAMPLE = {
    "first_name": "New_Student_Name",
    "last_name": "New_Student_Surname",
    "birth_year": 1900
}


GRADE_EXAMPLE = {
    "subject": "sport",
    "grade": 1
}


def validation_student_id_exception(students: Dict[int, Student], requested_id: int):
    try:
        students[requested_id]
    except KeyError:
        raise HTTPException(status_code=404, detail=f"Student #{requested_id} not found. Try to entry valid id")


@router.get("/{student_id}", response_model=Union[dict, ApiStudent], status_code=status.HTTP_200_OK)
def get_student(student_id: int):
    _, students, _ = read_all_data()
    validation_student_id_exception(students, student_id)
    return StudentManager.get_api_student_from_student(students[student_id])


@router.get("/{student_id}/stats/", status_code=status.HTTP_200_OK)
def get_student_stats(student_id: int):
    _, students, _ = read_all_data()
    validation_student_id_exception(students, student_id)
    student = students[student_id]
    if len(student.grades) == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Student has not any grades yet. Check students/{student_id}/grades"
            )
    return StudentManager.get_api_student_stats_from_student(student)


@router.get("/{student_id}/grades/", status_code=status.HTTP_200_OK)
def get_student_grades(student_id: int):
    _, students, _ = read_all_data()
    validation_student_id_exception(students, student_id)
    student_api_grades = StudentManager.get_api_student_grades_from_student(students[student_id])
    return {
        "grades_count": len(student_api_grades.grades),
        "grades": student_api_grades.grades
    }


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_student(student_api: ApiNewStudent = Body(example=STUDENT_EXAMPLE)):
    student = StudentManager.get_student_from_api_new_student(student_api)
    sc = StudentController(student)
    sc.save()
    return StudentManager.get_api_student_from_student(student)


@router.get("/{student_id}/grades/{grade_id}", status_code=status.HTTP_200_OK)
def get_student_grade_by_id(student_id: int, grade_id: int):
    _, students, _ = read_all_data()
    validation_student_id_exception(students, student_id)
    student = students[student_id]
    grade = student.grades.get(grade_id)
    if not grade:
        return {"error": f"The grade #{grade_id} does not belong to the student #{student_id}."}
    return GradeManager.get_api_grade_from_grade(grade)


@router.post("/{student_id}/grades/", status_code=status.HTTP_201_CREATED)
def create_grade(student_id: int, new_grade: ApiNewGrade = Body(example=GRADE_EXAMPLE)):
    _, students, _ = read_all_data()
    validation_student_id_exception(students, student_id)
    grade = GradeManager.get_grade_from_api_new_grade(api_grade=new_grade)
    grade.student_id = student_id
    sc = GradeController(grade)
    sc.save(student_id)
    return GradeManager.get_api_grade_from_grade(grade)


@router.delete("/{student_id}/", status_code=status.HTTP_204_NO_CONTENT)
def del_student_with_grades(student_id: int):
    _, students, _ = read_all_data()
    validation_student_id_exception(students, student_id)
    student = students[student_id]
    sc = StudentController(student)
    sc.delete()


