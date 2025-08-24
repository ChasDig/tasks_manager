from uuid import UUID

from fastapi import APIRouter, status, Depends, Response
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_pg_session
from businesses_models.v1 import TasksBusinessModel
from dependencies import get_page_params, get_sort_params
from dependencies.v1 import get_tasks_filters_request
from models.api_models import (
    TaskDataByIDResponse,
    PageParams,
    TasksFiltersRequest,
    SortParams,
    PagedResponse,
)

router = APIRouter(
    prefix="/tasks",
    tags=["tasks"],
)


@router.get(
    "/{task_id}",
    status_code=status.HTTP_200_OK,
    response_model=TaskDataByIDResponse,
)
async def get_task_by_id(
    task_id: UUID,
    pg_session: AsyncSession = Depends(get_pg_session),
) -> TaskDataByIDResponse | Response:
    """
    Получение Task по ID.

    @type task_id: UUID
    @param task_id:
    @type pg_session: AsyncSession
    @param pg_session:

    @rtype task: TaskDataByIDResponse | Response
    @return task:
    """
    business_model = TasksBusinessModel(pg_session=pg_session)
    task = await business_model.get_by_id(task_id=task_id)

    if not task:
        return Response(
            status_code=status.HTTP_404_NOT_FOUND,
            content=f"Task by ID='{task_id}' not found",
        )

    return task


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=PagedResponse[TaskDataByIDResponse],
)
async def get_list_tasks(
    page_params: PageParams = Depends(get_page_params),
    sort_params: SortParams = Depends(get_sort_params),
    filters: TasksFiltersRequest = Depends(get_tasks_filters_request),
    pg_session: AsyncSession = Depends(get_pg_session),
) -> PagedResponse[TaskDataByIDResponse]:
    """
    Получение массива Tasks с использованием пагинации и фильтрации.

    @type page_params: Depends(get_page_params)
    @param page_params:
    @type sort_params: Depends(get_sort_params)
    @param sort_params:
    @type filters: Depends(get_tasks_filters_request)
    @param filters:
    @type pg_session: AsyncSession
    @param pg_session:

    @rtype tasks: PagedResponse[TaskDataByIDResponse]
    @return tasks:
    """
    business_model = TasksBusinessModel(pg_session=pg_session)
    tasks_response = await business_model.get_list(
        page_params=page_params,
        sort_params=sort_params,
        filters=filters,
    )

    return tasks_response
