from datetime import date, datetime
from typing import Annotated
from pydantic import BaseModel, ConfigDict, StringConstraints
from app.enums.task_status import TaskStatus, TaskPriority

class TaskBase(BaseModel):

    title: Annotated[str, StringConstraints(
        min_length=1,
        max_length=255,
        strip_whitespace=True),]

    description: Annotated[str, StringConstraints(
        max_length=1000, strip_whitespace=True)]  | None = None

    due_date: date | None = None

class TaskCreate(TaskBase):
    """
    Schema used while creating a task.
    """

    status: TaskStatus = TaskStatus.PENDING
    priority: TaskPriority = TaskPriority.HIGH


class TaskUpdate(BaseModel):
    """
    Schema used while updating a task.
    All fields are optional.
    """

    title: Annotated[
        str,
        StringConstraints(
            min_length=3,
            max_length=255,
            strip_whitespace=True,
        ),
    ] | None = None

    description: Annotated[
        str,
        StringConstraints(
            max_length=1000,
            strip_whitespace=True,
        ),
    ] | None = None

    status: TaskStatus | None = None

    priority: TaskPriority | None = None

    due_date: date | None = None


class TaskResponse(TaskBase):
    """
    Schema returned to the client.
    """

    id: int
    status: TaskStatus
    owner_id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


