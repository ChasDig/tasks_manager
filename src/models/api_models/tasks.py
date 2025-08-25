from datetime import datetime
from typing import Any
from uuid import UUID

from pydantic import BaseModel, Field

from models.pg_models.custom_enum import TaskStatusEnum
from models.pg_models.task_manager import Task


class CreateTaskRequest(BaseModel):
    """RequestData - Задача по ID."""

    title: str = Field(
        description="Наименование Задачи",
        examples=["Task 1"],
    )
    description: str = Field(
        description="Описание Задачи",
        examples=["Description Task 1"],
    )
    status: TaskStatusEnum | str = Field(
        description="Статус Задачи",
        examples=[TaskStatusEnum.create.value],
    )


class TaskDataResponse(BaseModel):
    """ResponseData - Задача по ID."""

    id: UUID | str = Field(
        description="UUID идентификатор Задачи",
        examples=["a1b2c3d4-e5f6-7890-abcd-ef1234567890"],
    )
    title: str = Field(
        description="Наименование Задачи",
        examples=["Task 1"],
    )
    description: str = Field(
        description="Описание Задачи",
        examples=["Description Task 1"],
    )
    status: TaskStatusEnum | str = Field(
        description="Статус Задачи",
        examples=[TaskStatusEnum.create.value],
    )
    created_at: datetime = Field(
        description="Дата создания Задачи",
        examples=["2025-08-24 14:08:52.000"],
    )
    updated_at: datetime = Field(
        description="Дата обновления Задачи",
        examples=["2025-08-24 14:08:52.000"],
    )


class TasksFiltersRequest(BaseModel):
    """RequestData - фильтры Задач по ID."""

    title: str | None = Field(
        default=None,
        description="Наименование Задачи",
        examples=["Task 1"],
    )
    status: TaskStatusEnum | None = Field(
        default=None,
        description="Статус Задачи",
        examples=[TaskStatusEnum.create.value],
    )

    def correlate_with_alchemy(self) -> list[Any]:
        """
        Преобразование фильтров в SQLAlchemy-фильтры для запроса.

        @rtype correlated: list[Any]
        @return correlated:
        """
        correlated = list()

        if self.title:
            correlated.append(
                Task.title == self.title,
            )

        if self.status:
            correlated.append(Task.status == self.status.value)

        return correlated


class UpdateTaskRequest(BaseModel):
    """RequestData - Обновление Задачи."""

    title: str = Field(
        description="Наименование Задачи",
        examples=["Task 1"],
    )
    description: str = Field(
        description="Описание Задачи",
        examples=["Description Task 1"],
    )
    status: TaskStatusEnum | str = Field(
        description="Статус Задачи",
        examples=[TaskStatusEnum.in_process.value],
    )
