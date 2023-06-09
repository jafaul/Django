from typing import Optional

GroupIdType = int


class Group:
    def __init__(self, name: str, group_id: Optional[GroupIdType] = None, students: Optional[dict] = None):
        self.group_id = group_id
        self.name = name
        if students is None:
            self.students = {}
        else:
            self.students = students


    def __str__(self):
        return f"group_id: {self.group_id},\n"\
               f"name: {self.name},\n"\
               f"students: {self.students}"