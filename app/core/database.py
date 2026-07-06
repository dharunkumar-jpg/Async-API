from collections.abc import AsyncGenerator
from sqlalchemy.ext.asyncio import (AsyncSession,async_sessionmaker,create_async_engine,)
from sqlalchemy.orm import DeclarativeBase
from app.core.config import get_settings

settings = get_settings()

class Base(DeclarativeBase):
    """
    Base class for all SQLAlchemy models.
    """
    pass

engine = create_async_engine(
    settings.DATABASE_URL,
    echo=False,
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Provides an asynchronous database session per request.
    """
    async with AsyncSessionLocal() as session:
        yield session

        # poo_pre_ping it is used to send a test query, it will let the connection to be idle