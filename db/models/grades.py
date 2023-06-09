from typing import Optional

from db.models.students import StudentIdType

SubjectType = str
GradeIdType = int

class Grade:
    def __init__(
            self,
            subject: SubjectType,
            grade: int,
            date_grade: Optional[str] = None,
            grade_id: Optional[GradeIdType] = None,
            student_id: Optional[StudentIdType] = None
    ):
        self.grade_id = grade_id
        self.subject = subject
        self.grade = grade
        self.date_grade = date_grade
        self.student_id = student_id
        self.student = None


    def __str__(self):
        return f"grade_id: {self.grade_id},\n" \
               f"subject: {self.subject},\n" \
               f"grade: {self.grade},\n" \
               f"date_grade: {self.date_grade},\n" \
               f"student_id: {self.student_id}"