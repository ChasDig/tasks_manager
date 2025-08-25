from typing import Annotated
from uuid import UUID

from fastapi import Body, Depends, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_pg_session
from models.api_models import (
    CreateTaskRequest,
    TasksFiltersRequest,
    UpdateTaskRequest,
)
from models.pg_models import Task
from models.pg_models.custom_enum import TaskStatusEnum
from utils.custom_exception import (
    TaskAlreadyExistsError,
    TaskCreateError,
    TaskNotFoundError,
)


async def get_tasks_filters_request(
    title: str | None = Query(
        default=None,
        description="Наименование Задачи",
        examples=["Task 1"],
    ),
    status: TaskStatusEnum | None = Query(
        default=None,
        description="Статус Задачи",
        examples=[TaskStatusEnum.create.name],
    ),
) -> TasksFiltersRequest:
    return TasksFiltersRequest(title=title, status=status)


async def check_task_before_create(
    task_data: Annotated[CreateTaskRequest, Body()],
    pg_session: AsyncSession = Depends(get_pg_session),
) -> CreateTaskRequest:
    # Проверка: статус Задачи
    if task_data.status not in TaskStatusEnum.statuses_for_create():
        detail = f"Not valid status(must {TaskStatusEnum.statuses_for_create})"
        raise TaskCreateError(detail=detail)

    # Проверка: наличие не завершенной Задачи с таким же наименованием
    stmt = select(
        Task,
    ).where(
        Task.title == task_data.title,
        Task.status != TaskStatusEnum.completed.value,
    )
    query = await pg_session.execute(stmt)

    if query.scalar_one_or_none():
        raise TaskAlreadyExistsError()

    return task_data


async def check_task_before_update(
    task_id: UUID,
    task_data: Annotated[UpdateTaskRequest, Body()],
    pg_session: AsyncSession = Depends(get_pg_session),
) -> UpdateTaskRequest:
    # Проверка: существование Задачи
    query = await pg_session.execute(select(Task).where(Task.id == task_id))
    task: Task = query.scalar_one_or_none()

    if not task:
        raise TaskNotFoundError()

    # Проверка: текущий статус Задачи
    if task_data.status not in TaskStatusEnum.current_statuses_for_update():
        raise TaskCreateError(
            detail=(
                "Not valid status(must be "
                f"{TaskStatusEnum.current_statuses_for_update()})"
            )
        )

    # Проверка: устанавливаемый статус Задачи
    if task_data.status not in TaskStatusEnum.new_statuses_for_update():
        raise TaskCreateError(
            detail=(
                "Not valid status(must be "
                f"{TaskStatusEnum.new_statuses_for_update()})"
            )
        )

    return task_data
