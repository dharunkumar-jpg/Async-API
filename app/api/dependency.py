from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import decode_access_token
from app.exceptions.custom_exceptions import (InvalidTokenException,
                                              UserNotFoundException)
from app.repositories.user_repository import UserRepository
from app.schemas.token import TokenPayload
from app.services.auth_service import AuthService
from app.services.task_service import TaskService
from app.services.user_service import UserService

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login",
)


def get_auth_service(
    session: AsyncSession = Depends(get_db),
) -> AuthService:
    """
    Return an AuthService instance.
    """
    return AuthService(session)


def get_user_service(
    session: AsyncSession = Depends(get_db),
) -> UserService:
    """
    Return a UserService instance.
    """
    return UserService(session)


def get_task_service(
    session: AsyncSession = Depends(get_db),
) -> TaskService:
    """
    Return a TaskService instance.
    """
    return TaskService(session)


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    session: AsyncSession = Depends(get_db),
):
    """
    Retrieve the currently authenticated user.
    """

    payload = decode_access_token(token)

    try:
        token_data = TokenPayload(**payload)
    except ValidationError as exc:
        raise InvalidTokenException() from exc

    user_repository = UserRepository(session)

    user = await user_repository.get_by_id(
        int(token_data.sub),
    )

    if user is None:
        raise UserNotFoundException()

    return user