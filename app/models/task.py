from datetime import date
from sqlalchemy import Date, Enum, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base
from app.mixins.timestamp_mixin import TimestampMixin
from app.enums.task_status import TaskStatus,TaskPriority


class Task(Base, TimestampMixin):
    __tablename__ = 'tasks'
#mapped is generic type, it is type hinting logic
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=False)
    status: Mapped[TaskStatus] = mapped_column(Enum(TaskStatus), default=TaskStatus.PENDING, nullable=False)
    priority: Mapped[int] = mapped_column(Enum(TaskPriority), default=0, nullable=False)
    due_date: Mapped[date | None] = mapped_column(Date, nullable=False)
    owner_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)
    owner = relationship('User', back_populates='tasks')
