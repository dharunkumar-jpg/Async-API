from fastapi import APIRouter, Depends, status

from app.api.dependency import get_current_user, get_task_service
from app.models.user import User
from app.schemas.task import TaskCreate, TaskResponse, TaskUpdate
from app.services.task_service import TaskService

router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"],
)

@router.post(
    "",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_task(
    task: TaskCreate,
    current_user: User = Depends(get_current_user),
    task_service: TaskService = Depends(get_task_service),
) -> TaskResponse:
    """
    Create a new task.
    """
    return await task_service.create_task(
        task,
        current_user.id,
    )


@router.get(
    "",
    response_model=list[TaskResponse],
)
async def get_tasks(
    current_user: User = Depends(get_current_user),
    task_service: TaskService = Depends(get_task_service),
) -> list[TaskResponse]:
    """
    Get all tasks for the authenticated user.
    """
    return await task_service.get_tasks_by_owner(
        current_user.id,
    )


@router.get(
    "/{task_id}",
    response_model=TaskResponse,
)
async def get_task(
    task_id: int,
    current_user: User = Depends(get_current_user),
    task_service: TaskService = Depends(get_task_service),
) -> TaskResponse:
    """
    Get a task by ID.
    """
    return await task_service.get_by_owner_and_id(
        task_id,
        current_user.id,
    )


@router.put(
    "/{task_id}",
    response_model=TaskResponse,
)
async def update_task(
    task_id: int,
    task: TaskUpdate,
    current_user: User = Depends(get_current_user),
    task_service: TaskService = Depends(get_task_service),
) -> TaskResponse:
    """
    Update a task.
    """
    return await task_service.update_task(
        task_id,
        current_user.id,
        task,
    )


@router.delete(
    "/{task_id}",
    status_code= 204
)
async def delete_task(
    task_id: int,
    current_user: User = Depends(get_current_user),
    task_service: TaskService = Depends(get_task_service),
) -> None:
    """
    Delete a task.
    """
    await task_service.delete_task(
        task_id,
        current_user.id,
    )