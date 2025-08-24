from fastapi import Query

from models.api_models import TasksFiltersRequest
from models.pg_models.custom_enum import TaskStatusEnum


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
    )
) -> TasksFiltersRequest:
    return TasksFiltersRequest(title=title, status=status)
