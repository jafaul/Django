from pydantic import BaseModel


class ApiGrade(BaseModel):
    id: int
    subject: str
    grade: int
    date: str


class ApiNewGrade(BaseModel):
    subject: str
    grade: int


