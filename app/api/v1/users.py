from fastapi import APIRouter, Request,Depends, status

from app.api.dependency import (
    get_current_user,
    get_user_service,
)
from app.models.user import User
from app.schemas.user import UserResponse,UserUpdate
from app.services.user_service import UserService
from app.schemas.user import ChangePassword
from app.api.dependency import get_auth_service
from app.services.auth_service import AuthService
from app.core.rate_limiter import limiter

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.get(
    "/me",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
)
async def get_current_user_profile(
    current_user: User = Depends(get_current_user),
) -> UserResponse:
    """
    Get the currently authenticated user's profile.
    """
    return current_user


@router.get(
    "/{user_id}",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
)
async def get_user(
    user_id: int,
    user_service: UserService = Depends(get_user_service),
) -> UserResponse:
    """
    Get a user by ID.
    """
    return await user_service.get_user_by_id(user_id)

@router.put(
    "/me",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
)
async def update_current_user(
    user_data: UserUpdate,
    current_user: User = Depends(get_current_user),
    user_service: UserService = Depends(get_user_service),
) -> UserResponse:
    """
    Update the currently authenticated user's profile.
    """
    return await user_service.update_user(
        current_user.id,
        user_data,
    )

@router.put(
    "/change-password",
    status_code=status.HTTP_200_OK,
)
@limiter.limit("5/minute")
async def change_password(
    request: Request,
    password_data: ChangePassword,
    current_user: User = Depends(get_current_user),
    auth_service: AuthService = Depends(get_auth_service),
) -> dict[str, str]:
    """
    Change the password for the authenticated user.
    """
    await auth_service.change_password(
        current_user,
        password_data,
    )

    return {
        "message": "Password changed successfully."
    }