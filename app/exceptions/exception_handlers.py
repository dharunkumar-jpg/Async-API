from fastapi import FastAPI
from fastapi import Request
from fastapi.responses import JSONResponse
from app.exceptions.custom_exceptions import (
    TaskNotFoundException,
    UserAlreadyExistsException,
    UserNotFoundException,
    InvalidTokenException,
    InvalidCredentialsException
)

async def user_already_exists_exception_handler(
    request: Request,
    exc: UserAlreadyExistsException,
) -> JSONResponse:
    return JSONResponse(
        status_code=409,
        content={"detail": exc.message},
    )


async def user_not_found_exception_handler(
    request: Request,
    exc: UserNotFoundException,
) -> JSONResponse:
    return JSONResponse(
        status_code=404,
        content={"detail": exc.message},
    )


async def task_not_found_exception_handler(
    request: Request,
    exc: TaskNotFoundException,
) -> JSONResponse:
    return JSONResponse(
        status_code=404,
        content={"detail": exc.message},
    )

async def invalid_token_exception_handler(
    request: Request,
    exc: InvalidTokenException,
) -> JSONResponse:
    return JSONResponse(
        status_code=401,
        content={
            "detail": exc.message,
        },
    )

async def invalid_credentials_exception_handler(
    request: Request,
    exc: InvalidCredentialsException,
) -> JSONResponse:
    return JSONResponse(
        status_code=400 ,
        content={
            "detail": exc.message,
        },
    )

def register_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(
        UserAlreadyExistsException,
        user_already_exists_exception_handler,
    )
    app.add_exception_handler(
        UserNotFoundException,
        user_not_found_exception_handler,
    )
    app.add_exception_handler(
        TaskNotFoundException,
        task_not_found_exception_handler,
    )
    app.add_exception_handler(
        InvalidTokenException,
        invalid_token_exception_handler,
    )
    app.add_exception_handler(
        InvalidCredentialsException,
        invalid_credentials_exception_handler,
    )