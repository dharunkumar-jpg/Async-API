from typing import Generic, TypeVar

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import Base

ModelType = TypeVar("ModelType", bound=Base)


class BaseRepository(Generic[ModelType]):
    """
    Generic repository providing common CRUD operations.
    """

    def __init__(self,session: AsyncSession,model: type[ModelType],) -> None:
        self.session = session
        self.model = model

    async def create(self,obj: ModelType,) -> ModelType:
        """
        Add a new object to the database session.
        """
        self.session.add(obj)
        await self.session.flush()
        await self.session.refresh(obj)
        return obj

    async def get_by_id(self,obj_id: int,) -> ModelType | None:
        """
        Retrieve an object by its primary key.
        """
        result = await self.session.execute(
            select(self.model).where(self.model.id == obj_id)
        )
        return result.scalar_one_or_none()

    async def get_all(self) -> list[ModelType]:
        """
        Retrieve all records.
        """
        result = await self.session.execute(
            select(self.model)
        )
        return list(result.scalars().all())

    async def update(self,obj: ModelType,) -> ModelType:
        """
        Update an existing object.
        """
        await self.session.flush()
        await self.session.refresh(obj)
        return obj

    async def delete(self,obj: ModelType,) -> None:
        """
        Delete an object.
        """
        await self.session.delete(obj)
        await self.session.flush()