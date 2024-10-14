from enum import Enum as PyEnum


class TaskStatus(PyEnum):
    NEW = 'New'
    IN_PROGRESS = 'In Progress'
    COMPLETED = 'Completed'
