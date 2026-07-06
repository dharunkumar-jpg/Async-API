from enum import Enum


class TaskStatus(str, Enum):

    TODO = "start"
    PENDING = "pending"
    COMPLETED = "completed"

class TaskPriority(str, Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
