from fastapi import Query

from models.api_models import PageParams, SortParams
from utils import SortEnum


async def get_page_params(
    page: int = Query(
        default=1,
        ge=1,
        description="Номер страницы",
    ),
    size: int = Query(
        default=15,
        ge=1,
        lt=100,
        description="Кол-во элементов на странице",
    ),
) -> PageParams:
    return PageParams(page=page, size=size)


async def get_sort_params(
    sort_by: str = Query(
        default="created_at",
        description="Поле для сортировки",
    ),
    sort_order: SortEnum = Query(
        default=SortEnum.desc,
        description=f"Порядок сортировки ({SortEnum.names()})",
    ),
) -> SortParams:
    return SortParams(sort_by=sort_by, sort_order=sort_order)
