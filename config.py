import os

from pydantic import BaseSettings

from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    grades_file: str = os.environ["GRADES_FILE"]
    students_file: str = os.environ["STUDENTS_FILE"]
    groups_file: str = os.environ["GROUPS_FILE"]
    students_in_groups_file: str = os.environ["STUDENTS_IN_GROUPS_FILE"]

    class Config:
        env_file = ".env"




