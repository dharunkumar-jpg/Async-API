from sqlalchemy.ext.asyncio import AsyncSession
from app.core.security import (
    create_access_token,
    hash_password,
    verify_password,
)
from app.exceptions.custom_exceptions import (
    InvalidCredentialsException,
    UserAlreadyExistsException,
    InvalidPasswordException,
    SamePasswordException,
)
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.token import Token
from app.schemas.user import UserCreate
from app.services.base_services import BaseService
from app.schemas.user import ChangePassword
from app.core.security import hash_password, verify_password



class AuthService(BaseService):
    """
    Service responsible for authentication operations.
    """

    def __init__(self,session: AsyncSession,) -> None:
        super().__init__(session)
        self.user_repository = UserRepository(session)

    async def register(self,user_data: UserCreate,) -> User:
        """
        Register a new user.
        """

        existing_user = await self.user_repository.get_by_email(
            user_data.email,
        )

        if existing_user:
            raise UserAlreadyExistsException()

        user = User(
            full_name=user_data.full_name,
            email=user_data.email,
            hashed_password=hash_password(user_data.password),
        )

        try:
            await self.user_repository.create(user)
            await self.commit()
            return user

        except Exception:
            await self.rollback()
            raise

    async def login(self,email: str,password: str,) -> Token:
        """
        Authenticate a user and return an access token.
        """

        user = await self.user_repository.get_by_email(
            email,
        )

        if (
            user is None
            or not verify_password(
                password,
                user.hashed_password,
            )
        ):
            raise InvalidCredentialsException()

        access_token = create_access_token(
            {
                "sub": str(user.id),
            }
        )

        return Token(
            access_token=access_token,
            token_type="bearer",
        )

    async def change_password(self,user: User,password_data: ChangePassword,) -> None:
            """
            Change the password for the authenticated user.
            """

            if not verify_password(
                    password_data.current_password,
                    user.password,
            ):
                raise InvalidPasswordException()

            if password_data.current_password == password_data.new_password:
                raise SamePasswordException()

            user.password = hash_password(
                password_data.new_password,
            )

            try:
                await self.user_repository.update(user)
                await self.commit()

            except Exception:
                await self.rollback()
                raise