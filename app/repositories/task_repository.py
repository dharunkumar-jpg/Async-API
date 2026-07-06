from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.enums.task_status import TaskStatus
from app.models.task import Task
from app.repositories.base_repository import BaseRepository


class TaskRepository(BaseRepository[Task]):
    """
    Repository for task-specific database operations.
    """

    def __init__(self,session: AsyncSession,) -> None:
        super().__init__(session, Task)

    async def get_tasks_by_owner(self,owner_id: int,) -> list[Task]:
        """
        Retrieve all tasks belonging to a user.
        """
        result = await self.session.execute(
            select(Task).where(Task.owner_id == owner_id)
        )
        return list(result.scalars().all())

    async def get_tasks_by_status(self, status: TaskStatus, ) -> list[Task]:
        """
        Retrieve all tasks with the given status.
        """
        result = await self.session.execute(
            select(Task).where(Task.status == status)
        )
        return list(result.scalars().all())

    async def get_by_owner_and_id(self,task_id: int,owner_id: int,) -> Task | None:
        """
        Retrieve a task by its ID and owner ID.
        """
        result = await self.session.execute(
            select(Task).where(
                Task.id == task_id,
                Task.owner_id == owner_id,
            )
        )

        return result.scalar_one_or_none()