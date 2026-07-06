from sqlalchemy import Boolean, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.mixins.timestamp_mixin import TimestampMixin


class User(Base, TimestampMixin):

    """
    Represents an application user
    """

    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    full_name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, index=True ,nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(100), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    tasks = relationship('Task', back_populates='owner',cascade="all, delete-orphan")





