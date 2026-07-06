from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserUpdate
from app.services.base_services import BaseService

# from app.exceptions.custom_exceptions import UserAlreadyExistsException

class UserService(BaseService):
    """
    Service containing user-related business logic.
    """

    def __init__(self,session: AsyncSession,) -> None:
        super().__init__(session)
        self.user_repository = UserRepository(session)

    async def get_user_by_id(self,user_id: int,) -> User | None:
        """
        Retrieve a user by ID.
        """
        return await self.user_repository.get_by_id(user_id)

    async def update_user(
            self,
            user_id: int,
            user_data: UserUpdate,
    ) -> User:
        """
        Update an existing user.
        """

        user = await self.get_user_by_id(user_id)

        update_data = user_data.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(user, field, value)

        await self.user_repository.update(user)
        await self.commit()

        return user