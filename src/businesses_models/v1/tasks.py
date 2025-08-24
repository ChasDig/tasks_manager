from uuid import UUID

from sqlalchemy import select, func, Sequence
from sqlalchemy.ext.asyncio import AsyncSession

from models.pg_models import Task
from models.api_models import (
    TaskDataByIDResponse,
    PageParams,
    SortParams,
    TasksFiltersRequest,
    PagedResponse,
)


class TasksBusinessModel:
    """BusinessModel: Задача."""

    def __init__(self, pg_session: AsyncSession) -> None:
        self._pg_session = pg_session

    async def get_by_id(
        self,
        task_id: str | UUID,
    ) -> TaskDataByIDResponse | None:
        """
        Получение Task по ID.

        @type task_id: UUID
        @param task_id:

        @rtype task: TaskDataByIDResponse | None
        @return task:
        """
        stmt = (
            select(
                Task,
            ).where(
                Task.id == task_id,
            )
        )

        query = await self._pg_session.execute(stmt)
        if task := query.scalar_one_or_none():
            return TaskDataByIDResponse(
                id=task.id,
                title=task.title,
                description=task.description,
                status=task.status,
            )

        return None

    async def get_list(
        self,
        page_params: PageParams,
        sort_params: SortParams,
        filters: TasksFiltersRequest,
    ) -> PagedResponse[TaskDataByIDResponse]:
        """
        Получение массива Tasks с использованием пагинации, сортировки и
        фильтрации.

        @type page_params: PageParams
        @param page_params:
        @type sort_params: SortParams
        @param sort_params:
        @type filters: TasksFiltersRequest
        @param filters:

        @rtype tasks_response: PagedResponse[TaskDataByIDResponse]
        @return tasks_response:
        """
        alchemy_filters = filters.correlate_with_alchemy()

        # Total pages
        total_pages_stmt = (
            select(
                func.count(
                    Task.id,
                ),
            ).select_from(
                Task
            ).where(
                *alchemy_filters,
            )
        )
        total_pages_query = await self._pg_session.execute(total_pages_stmt)
        total_pages = total_pages_query.scalar()

        # Tasks
        tasks_stmt = (
            select(
                Task,
            ).where(
                *alchemy_filters,
            ).offset(
                page_params.offset,
            ).limit(
                page_params.limit,
            ).order_by(
                sort_params.correlate_with_alchemy(Task),
            )
        )
        tasks_query = await self._pg_session.execute(tasks_stmt)
        tasks: Sequence[Task] = tasks_query.scalars().all()

        return PagedResponse.create(
            items=tasks,
            tota_count=total_pages,
            page_params=page_params,
            sort_params=sort_params,
        )
