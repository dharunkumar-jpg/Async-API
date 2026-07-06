from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.repositories.base_repository import BaseRepository


class UserRepository(BaseRepository[User]):
    """
    Repository for user-specific database operations.
    """

    def __init__(self,session: AsyncSession,) -> None:
        super().__init__(session, User)

    async def get_by_email(self,email: str,) -> User | None:
        """
        Retrieve a user by email address.
        """
        result = await self.session.execute(
            select(User).where(User.email == email)
        )
        return result.scalar_one_or_none()