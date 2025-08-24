from uuid import UUID

from sqlalchemy import select, func, Sequence, update
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from businesses_models.base import BaseBusinessModel
from core.app_logger import logger
from models.pg_models import Task
from models.api_models import (
    TaskDataResponse,
    PageParams,
    SortParams,
    TasksFiltersRequest,
    PagedResponse,
    CreateTaskRequest,
    UpdateTaskRequest,
)
from utils.custom_exception import TaskCreateError, TaskUpdateError


class TasksBusinessModel(BaseBusinessModel):
    """BusinessModel: Задача."""

    def __init__(self, pg_session: AsyncSession) -> None:
        self._pg_session = pg_session

    async def create(self, task_data: CreateTaskRequest) -> TaskDataResponse:
        """
        Создание Task.

        @type task_data: CreateTaskRequest
        @param task_data:

        @rtype task: TaskDataResponse
        @return task:
        """
        new_task = Task(**task_data.model_dump())

        try:
            self._pg_session.add(new_task)
            await self._pg_session.commit()
            await self._pg_session.refresh(new_task)

            return self._get_task_for_response(task=new_task)

        except SQLAlchemyError as ex:
            logger.error(f"[!]Error create Task: {ex}")
            await self._pg_session.rollback()

            raise TaskCreateError()

    async def get_by_id(
        self,
        task_id: str | UUID,
    ) -> TaskDataResponse | None:
        """
        Получение Task по ID.

        @type task_id: UUID
        @param task_id:

        @rtype task: TaskDataResponse | None
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
            return self._get_task_for_response(task=task)

        return None

    async def get_list(
        self,
        page_params: PageParams,
        sort_params: SortParams,
        filters: TasksFiltersRequest,
    ) -> PagedResponse[TaskDataResponse]:
        """
        Получение массива Tasks с использованием пагинации, сортировки и
        фильтрации.

        @type page_params: PageParams
        @param page_params:
        @type sort_params: SortParams
        @param sort_params:
        @type filters: TasksFiltersRequest
        @param filters:

        @rtype tasks_response: PagedResponse[TaskDataResponse]
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
        search_tasks_stmt = (
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
        search_tasks_query = await self._pg_session.execute(search_tasks_stmt)
        search_tasks: Sequence[Task] = search_tasks_query.scalars().all()
        tasks = [self._get_task_for_response(task=t) for t in search_tasks]

        return PagedResponse.create(
            items=tasks,
            tota_count=total_pages,
            page_params=page_params,
            sort_params=sort_params,
        )

    async def update(
        self,
        task_id: UUID | str,
        task_data: UpdateTaskRequest,
    ) -> TaskDataResponse:
        """
        Частичное обновление Task.

        @type task_id: UUID
        @param task_id:
        @type task_data: CreateTaskRequest
        @param task_data:

        @rtype task: TaskDataResponse
        @return task:
        """
        stmt = (
            update(
                Task,
            ).where(
                Task.id == task_id,
            ).values(
                **task_data.model_dump(),
            )
        )

        try:
            await self._pg_session.execute(stmt)
            await self._pg_session.commit()

            query = await self._pg_session.execute(
                select(
                    Task,
                ).where(
                    Task.id == task_id,
                )
            )
            task: Task = query.scalar_one_or_none()

            return self._get_task_for_response(task=task)


        except SQLAlchemyError as ex:
            logger.error(f"[!]Error update Task: {ex}")
            await self._pg_session.rollback()

            raise TaskUpdateError()

    @staticmethod
    def _get_task_for_response(task: Task) -> TaskDataResponse:
        """
        Получение данных из Task(БД) для отправки в качестве ответа на запрос.

        @type task: Task
        @param task:

        @rtype: TaskDataResponse
        @return:
        """
        return TaskDataResponse(
            id=task.id,
            title=task.title,
            description=task.description,
            status=task.status,
            created_at=task.created_at,
            updated_at=task.updated_at,
        )
