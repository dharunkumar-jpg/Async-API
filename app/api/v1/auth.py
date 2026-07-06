from fastapi import APIRouter, Depends, Request, status
from fastapi.security import OAuth2PasswordRequestForm
from app.api.dependency import get_auth_service
from app.core.rate_limiter import limiter
from app.schemas.token import Token
from app.schemas.user import UserCreate, UserResponse
from app.services.auth_service import AuthService

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
@limiter.limit("3/minute")
async def register(
        request: Request,
        user: UserCreate,
    auth_service: AuthService = Depends(get_auth_service),
) -> UserResponse:
    """
    Register a new user.
    """
    return await auth_service.register(user)


from fastapi import APIRouter, Depends, Request, status


@router.post(
    "/login",
    response_model=Token,
    status_code=status.HTTP_200_OK,
)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    auth_service: AuthService = Depends(get_auth_service),
) -> Token:
    """
    Authenticate a user and return an access token.
    """
    return await auth_service.login(
        email=form_data.username,
        password=form_data.password,
    )