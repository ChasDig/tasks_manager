from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base, DatetimeStampedMixin
from .custom_enum import Schemas, task_status_enum, TaskStatusEnum


class Task(Base, DatetimeStampedMixin):
    """Postgres модель - Задача."""

    __tablename__ = "task"
    __table_args__ = {"schema": Schemas.task_manager.value}

    title: Mapped[str] = mapped_column(
        String(256),
        nullable=False,
        doc="Наименование задачи",
    )
    description: Mapped[str] = mapped_column(
        Text,
        nullable=False,
        doc="Описание задачи",
    )
    status: Mapped[str] = mapped_column(
        task_status_enum,
        nullable=False,
        default=TaskStatusEnum.create.value,
        doc="Статус задачи",
    )

    def __repr__(self) -> str:
        return self.title
