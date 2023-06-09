import csv
from datetime import date
from typing import List, Dict, Tuple

from config import Settings
from db.models.grades import Grade, GradeIdType
from db.models.groups import Group, GroupIdType
from db.models.students import Student, StudentIdType

settings = Settings()


def read_groups() -> Dict[int, Group]:
    with open(settings.groups_file, "r") as groups_csv:
        r_groups = csv.DictReader(groups_csv)
        groups = {}
        for r_group in r_groups:
            group = Group(
                group_id=int(r_group["id"]),
                name=r_group["name"]
            )
            groups[group.group_id] = group
        return groups


def read_students() -> Dict[int, Student]:
    with open(settings.students_file, "r") as students_csv:
        r_students = csv.DictReader(students_csv)
        students = {}
        for r_student in r_students:
            student = Student(
                student_id=int(r_student["id"]),
                first_name=r_student["first_name"],
                last_name=r_student["last_name"],
                birth_year=r_student["birth_year"]
            )
            students[student.student_id] = student
        return students


Headers = str


def read_grades() -> Dict[int, Grade]:
    with open(str(settings.grades_file), "r") as grades_csv:
        r_grades = csv.DictReader(grades_csv)
        grades = {}
        for r_grade in r_grades:
            grade  = Grade(
                grade_id=int(r_grade["id"]),
                subject=r_grade["subject"],
                grade=int(r_grade["grade"]),
                date_grade=r_grade["date"],
                student_id=int(r_grade["student_id"])
            )
            grades[grade.grade_id] = grade
        return grades


def read_group_student_relation() -> List[Tuple[int, int]]:
    with open(settings.students_in_groups_file, "r") as students_in_groups_csv:
        students_in_groups_data = list(csv.reader(students_in_groups_csv, delimiter=","))[1:]
        relations = []
        for data_index in range(len(students_in_groups_data)):
            student_id = int(students_in_groups_data[data_index][0])
            group_id = int(students_in_groups_data[data_index][1])
            relations.append((student_id, group_id))
        return relations


def fill_groups_with_students(
        groups: Dict[int, Group], students: Dict[int, Student], relations: List[Tuple[int, int]]
):
    for student_id, group_id in relations:
        group = groups.get(group_id)
        student = students.get(student_id)
        if not group or not student:
            print("Value error. Edit csv file. Check student_id and group_id")
            return
        group: Group
        student: Student
        group.students[student_id] = student


def fill_students_with_grades(students: Dict[int, Student], grades: Dict[int, Grade]):
    for grade in grades.values():
        student = students.get(grade.student_id)
        if not student:
            print("Error. Student not found. Edit csv file")
            return
        student: Student
        student.grades[grade.grade_id] = grade
        grade.student = student


def read_all_data() -> Tuple[Dict[int,Group], Dict[int, Student], Dict[int, Grade]]:
    groups = read_groups()
    students = read_students()
    grades = read_grades()
    relation = read_group_student_relation()
    fill_groups_with_students(groups, students, relation)
    fill_students_with_grades(students, grades)
    return groups, students, grades


def get_headers_by_file(csv_path: str) -> List[Headers]:
    with open(csv_path, "r") as csv_file:
        headers = list(csv.reader(csv_file, delimiter=","))[:1][0]
        return headers


def add_student(student: Student) -> StudentIdType:
    students_path = settings.students_file
    with open(students_path, "a+", newline='\n') as students_csv:
        headers = get_headers_by_file(students_path)
        writer = csv.DictWriter(students_csv, fieldnames=headers)
        students = read_students()
        for st in list(students.values())[-1:]:
            last_student_id = st.student_id
        new_student_id = last_student_id + 1
        writer.writerow({
            "id": new_student_id,
            "first_name": student.first_name,
            "last_name": student.last_name,
            "birth_year": student.birth_year
        })
        return new_student_id


def add_group_with_relations(group: Group, students_ids: List[StudentIdType]) -> Tuple[
    GroupIdType, Dict[StudentIdType, Student]
]:
    groups_path = settings.groups_file
    relations_path = settings.students_in_groups_file
    with open(groups_path, "a+", newline='\n') as groups_csv, open(relations_path, "a+", newline='\n') as relations_csv:
        writer = csv.DictWriter(groups_csv, fieldnames=get_headers_by_file(groups_path))
        groups = read_groups()
        for gr in list(groups.values())[-1:]:
            last_group_id = gr.group_id
        new_group_id = last_group_id + 1
        writer.writerow({
            "id": new_group_id,
            "name": group.name
        })

        writer = csv.DictWriter(relations_csv, fieldnames=get_headers_by_file(relations_path))
        students = {}
        db_students = read_students()
        for st_id in students_ids:
            student = db_students.get(st_id)
            student: Student
            students[st_id] = student
            writer.writerow({
                "student_id": st_id,
                "group_id": new_group_id
            })
        return new_group_id, students


def add_grade(grade: Grade) -> Tuple[GradeIdType, date]:
    grades_path = settings.grades_file
    with open(grades_path, "a+", newline='\n') as grades_csv:
        writer = csv.DictWriter(grades_csv, fieldnames=get_headers_by_file(grades_path))
        grades = read_grades()
        for gr in list(grades.values())[-1:]:
            last_grade_id = gr.grade_id
        new_grade_id = last_grade_id + 1
        date_today = date.today()
        writer.writerow({
            "id": new_grade_id,
            "subject": grade.subject,
            "grade": grade.grade,
            "date": date_today,
            "student_id": grade.student_id
        })
        return new_grade_id, date_today


def add_student_into_group_by_student_id(student_id: int, group_id: int) -> Student:
    db_groups, db_students, _ = read_all_data()
    relations_path = settings.students_in_groups_file
    with open(relations_path, "a+", newline='\n') as relations_csv:
        writer = csv.DictWriter(relations_csv, fieldnames=get_headers_by_file(relations_path))
        student = db_students.get(student_id)
        student: Student
        group = db_groups.get(group_id)
        group: Group
        group.students[student_id] = student
        writer.writerow({
            "student_id": student_id,
            "group_id": group_id
        })
        return student


def del_student_data_from_students(student_id: int):
    _, students, _ = read_all_data()
    del students[student_id]
    students_path = settings.students_file
    headers = get_headers_by_file(students_path)
    with open(students_path, 'w', newline='\n') as students_csv:
        writer = csv.DictWriter(students_csv, fieldnames=headers)
        writer.writeheader()
        for student in students.values():
            writer.writerow({
            "id": student.student_id,
            "first_name": student.first_name,
            "last_name": student.last_name,
            "birth_year": student.birth_year
            })


def rewrite_relation(new_relations):
    relation_path = settings.students_in_groups_file
    rel_headers = get_headers_by_file(relation_path)
    # relations = read_group_student_relation()
    with open(relation_path, "w", newline='\n') as relations_csv:
        writer = csv.DictWriter(relations_csv, fieldnames=rel_headers)
        writer.writeheader()
        for relation in new_relations:
            writer.writerow({
                "student_id": relation[0],
                "group_id": relation[1]
            })


def del_student_data_from_relations(student_id: int):
    relations = read_group_student_relation()
    for relation in relations:
        rel_student_id = relation[0]
        if rel_student_id == student_id:
            relations.remove(relation)
    rewrite_relation(relations)


def del_student_data_from_grades(student_id: int):
    _, _, grades = read_all_data()
    grades_path = settings.grades_file
    grades_headers = get_headers_by_file(grades_path)
    for grade in grades.copy().values():
        if grade.student_id == student_id:
            del grades[grade.grade_id]
    with open(grades_path, "w", newline='\n') as grades_csv:
        writer = csv.DictWriter(grades_csv, fieldnames=grades_headers)
        writer.writeheader()
        for grade in grades.values():
            writer.writerow({
                "id": grade.grade_id,
                "subject": grade.subject,
                "grade": grade.grade,
                "date": grade.date_grade,
                "student_id": grade.student_id
            })


def delete_all_student_data(student_id: int):
    del_student_data_from_grades(student_id)
    del_student_data_from_relations(student_id)
    del_student_data_from_students(student_id)


def del_group_from_groups(group_id: int):
    groups, _, _ = read_all_data()
    groups_path = settings.groups_file
    groups_headers = get_headers_by_file(groups_path)
    del groups[group_id]
    with open(groups_path, "w", newline="\n") as groups_csv:
        writer = csv.DictWriter(groups_csv, fieldnames=groups_headers)
        writer.writeheader()
        for group in groups.values():
            writer.writerow({
                "id": group.group_id,
                "name": group.name
            })

def del_group_students_relations(group_id: int):
    relations = read_group_student_relation()
    for relation in relations:
        if relation[1] == group_id:
            relations.remove(relation)
    rewrite_relation(relations)


def delete_all_group_data(group_id: int):
    del_group_students_relations(group_id)
    del_group_from_groups(group_id)


def delete_student_from_group(student_id: int, group_id: int):
    relations = read_group_student_relation()
    for relation in relations:
        if relation[0] == student_id and relation[1] == group_id:
            relations.remove(relation)
    rewrite_relation(relations)


def rewrite_group_name(group_id: int, new_name: str):
    groups, _, _ = read_all_data()
    groups_path = settings.groups_file
    groups_headers = get_headers_by_file(groups_path)
    for group in groups.values():
        if group.group_id == group_id:
            group.name = new_name
    with open(groups_path, "w", newline="\n") as groups_csv:
        writer = csv.DictWriter(groups_csv, fieldnames=groups_headers)
        writer.writeheader()
        for group in groups.values():
            writer.writerow({
                "id": group.group_id,
                "name": group.name
            })

# update name group
# remove student from group, remove/delete. "{student_id}"