from typing import Optional

StudentIdType = int


class Student:
    def __init__(self, *, first_name: str, last_name: str, birth_year: int, grades: Optional[dict] = None, student_id: Optional[StudentIdType] = None):
        self.student_id = student_id
        self.first_name = first_name
        self.last_name = last_name
        self.birth_year = birth_year
        if grades is None:
            self.grades = {}
        else:
            self.grades = grades


    def __str__(self):
        return f"student_id: {self.student_id},\n" \
               f"first_name: {self.first_name},\n" \
               f"last_name: {self.last_name},\n" \
               f"birth_year: {self.birth_year},\n" \
               f"grades: {self.grades}"