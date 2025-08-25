from uuid import UUID

from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from businesses_models.v1 import TasksBusinessModel
from database import get_pg_session
from dependencies import get_page_params, get_sort_params
from dependencies.v1 import (
    check_task_before_create,
    check_task_before_update,
    get_tasks_filters_request,
)
from models.api_models import (
    CreateTaskRequest,
    PagedResponse,
    PageParams,
    SortParams,
    TaskDataResponse,
    TasksFiltersRequest,
    UpdateTaskRequest,
)

router = APIRouter(
    prefix="/tasks",
    tags=["tasks"],
)


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=TaskDataResponse,
)
async def create_task(
    task_data: CreateTaskRequest = Depends(check_task_before_create),
    pg_session: AsyncSession = Depends(get_pg_session),
) -> TaskDataResponse:
    """
    Создание Task.

    @type task_data: CreateTaskRequest
    @param task_data:
    @type pg_session: AsyncSession
    @param pg_session:

    @rtype task: TaskDataResponse
    @return task:
    """
    business_model = TasksBusinessModel(pg_session=pg_session)
    task = await business_model.create(task_data=task_data)

    return task


@router.get(
    "/{task_id}",
    status_code=status.HTTP_200_OK,
    response_model=TaskDataResponse,
)
async def get_task_by_id(
    task_id: UUID,
    pg_session: AsyncSession = Depends(get_pg_session),
) -> TaskDataResponse | Response:
    """
    Получение Task по ID.

    @type task_id: UUID
    @param task_id:
    @type pg_session: AsyncSession
    @param pg_session:

    @rtype task: TaskDataResponse | Response
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
    response_model=PagedResponse[TaskDataResponse],
)
async def get_list_tasks(
    page_params: PageParams = Depends(get_page_params),
    sort_params: SortParams = Depends(get_sort_params),
    filters: TasksFiltersRequest = Depends(get_tasks_filters_request),
    pg_session: AsyncSession = Depends(get_pg_session),
) -> PagedResponse[TaskDataResponse]:
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

    @rtype tasks: PagedResponse[TaskDataResponse]
    @return tasks:
    """
    business_model = TasksBusinessModel(pg_session=pg_session)
    tasks_response = await business_model.get_list(
        page_params=page_params,
        sort_params=sort_params,
        filters=filters,
    )

    return tasks_response


@router.patch(
    "/{task_id}",
    status_code=status.HTTP_200_OK,
    response_model=TaskDataResponse,
)
async def update_task(
    task_id: UUID,
    task_data: UpdateTaskRequest = Depends(check_task_before_update),
    pg_session: AsyncSession = Depends(get_pg_session),
) -> TaskDataResponse:
    """
    Частичное обновление Task.

    @type task_id: UUID
    @param task_id:
    @type task_data: CreateTaskRequest
    @param task_data:
    @type pg_session: AsyncSession
    @param pg_session:

    @rtype task: TaskDataResponse
    @return task:
    """
    business_model = TasksBusinessModel(pg_session=pg_session)
    task = await business_model.update(task_id=task_id, task_data=task_data)

    return task


@router.delete(
    "/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_task(
    task_id: UUID,
    pg_session: AsyncSession = Depends(get_pg_session),
) -> None:
    """
    Удаление Task.

    @type task_id: UUID
    @param task_id:
    @type pg_session: AsyncSession
    @param pg_session:

    @rtype: None
    @return:
    """
    business_model = TasksBusinessModel(pg_session=pg_session)
    await business_model.delete(task_id=task_id)

    return None
