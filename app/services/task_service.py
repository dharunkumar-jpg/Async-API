from sqlalchemy.ext.asyncio import AsyncSession

from app.enums.task_status import TaskStatus
from app.exceptions.custom_exceptions import TaskNotFoundException
from app.models.task import Task
from app.repositories.task_repository import TaskRepository
from app.schemas.task import TaskCreate, TaskUpdate
from app.services.base_services import BaseService


class TaskService(BaseService):
    """
    Service containing task-related business logic.
    """

    def __init__(self,session: AsyncSession,) -> None:
        super().__init__(session)
        self.task_repository = TaskRepository(session)

    async def create_task(self,task_data: TaskCreate,owner_id: int,) -> Task:
        """
        Create a new task.
        """
        task = Task(
            title=task_data.title,
            description=task_data.description,
            status=task_data.status,
            priority=task_data.priority,
            due_date=task_data.due_date,
            owner_id=owner_id,
        )

        try:
            await self.task_repository.create(task)
            await self.commit()

            return task

        except Exception:
            await self.rollback()
            raise

    async def get_by_owner_and_id(self,task_id: int,owner_id: int,) -> Task | None:
        """
        Retrieve a task by ID.
        """
        task = await self.task_repository.get_by_owner_and_id(task_id,owner_id,)

        if task is None:
            raise TaskNotFoundException()

        return task
    async def get_tasks_by_owner(self,owner_id: int,) -> list[Task]:
        """
        Retrieve all tasks for a user.
        """
        return await self.task_repository.get_tasks_by_owner(owner_id)

    async def get_tasks_by_status(self,owner_id: int,status: TaskStatus,) -> list[Task]:
        """
        Retrieve all tasks for a user by status.
        """

        return await self.task_repository.get_by_status(
            owner_id,
            status,
        )

    async def update_task(self,task_id: int,owner_id: int,task_data: TaskUpdate,) -> Task:
        """
        Update an existing task.
        """

        task = await self.task_repository.get_by_owner_and_id(
            task_id,
            owner_id,
        )

        if task is None:
            raise TaskNotFoundException()

        update_data = task_data.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(task, field, value)

        try:
            await self.task_repository.update(task)
            await self.commit()
            return task

        except Exception:
            await self.rollback()
            raise

        async def delete_task(self,task_id: int,owner_id: int,) -> None:
            """
            Delete a task.
            """

            task = await self.task_repository.get_by_owner_and_id(
                task_id,
                owner_id,
            )

            if task is None:
                raise TaskNotFoundException()

            try:
                await self.task_repository.delete(task)
                await self.commit()

            except Exception:
                await self.rollback()
                raise