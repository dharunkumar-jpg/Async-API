import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware

from app.api.v1.router import api_router
from app.core.database import Base, engine
from app.core.rate_limiter import limiter
from app.exceptions.exception_handlers import register_exception_handlers
from app.middleware.logging import LoggingMiddleware

# from app.models.user import User
# from app.models.task import Task


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)

app = FastAPI(
    title="Task Management API",
    version="1.0.0",
    description="Production-ready Task Management API built with FastAPI.",
)

@app.on_event("startup")
async def startup() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# Register rate limiter
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded,_rate_limit_exceeded_handler,)

# Middleware
app.add_middleware(LoggingMiddleware)
app.add_middleware(SlowAPIMiddleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register custom exception handlers
register_exception_handlers(app)
# Register API routes
app.include_router(api_router)

@app.get("/")
def home():
    return {
        "message": "Task Manager API Running Successfully"
    }