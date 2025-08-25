from pydantic import BaseModel, Field
from typing import Generic, TypeVar, Type, Sequence, Any
from math import ceil

from sqlalchemy.orm import class_mapper

from models.pg_models import Base
from utils import SortEnum

DataT = TypeVar("DataT")


class SortParams(BaseModel):
    """Параметр выборки - сортировка."""

    sort_by: str = Field(
        default="created_at",
        description="Поле для сортировки",
    )
    sort_order: SortEnum = Field(
        default=SortEnum.desc,
        description=f"Порядок сортировки ({SortEnum.names()})",
    )

    def correlate_with_alchemy(self, model_class: Type[Base]) -> Any:
        """
        Преобразование параметров сортировки в SQLAlchemy-формат.

        @type model_class: Type[Base]
        @param model_class:

        @rtype: Any
        @return:
        """
        if not hasattr(model_class, self.sort_by):
            available_f = [c.key for c in class_mapper(model_class).columns]
            raise AttributeError(
                f"Field {self.sort_by} not found in "
                f"{model_class.model_name()}. Available fields: {available_f}"
            )

        field = getattr(model_class, self.sort_by)

        if self.sort_order == SortEnum.asc:
            return field.asc()

        else:
            return field.desc()


class PageParams(BaseModel):
    """Параметр выборки - параметры страницы."""

    page: int = Field(
        default=1,
        ge=1,
        description="Номер страницы",
    )
    size: int = Field(
        default=15,
        ge=1,
        lt=100,
        description="Кол-во элементов на странице",
    )

    @property
    def offset(self) -> int:
        """
        Отступ.

        @rtype: int
        @return:
        """
        return (self.page - 1) * self.size

    @property
    def limit(self) -> int:
        return self.size


class Pagination(BaseModel):
    """Параметр выборки - параметры пагинации."""

    page: int = Field(
        default=1,
        ge=1,
        description="Номер страницы",
    )
    size: int = Field(
        default=15,
        ge=1,
        lt=100,
        description="Кол-во элементов на странице",
    )
    sort_by: str = Field(
        default="created_at",
        description="Поле для сортировки",
    )
    sort_order: SortEnum = Field(
        default=SortEnum.desc,
        description="Порядок сортировки (asc/desc)",
    )
    total_items: int = Field(description="Общее кол-во элементов")
    total_pages: int = Field(description="Общее кол-во страниц")
    next_page: int | None = Field(
        default=None,
        description="Следующая страница",
    )
    past_page: int | None = Field(
        default=None,
        description="Предыдущая страница",
    )

class PagedResponse(BaseModel, Generic[DataT]):
    """Параметр выборки - параметры пагинации + возвращаемые значения."""

    data: Sequence[DataT] = Field(description="Возвращаемые данные")
    pagination: Pagination = Field(description="Данные пагинации")

    @classmethod
    def create(
        cls,
        items: Sequence[DataT],
        tota_count: int,
        page_params: PageParams,
        sort_params: SortParams,
    ) -> "PagedResponse":
        total_pages = (
            ceil(tota_count / page_params.size) if tota_count > 0 else 1
        )

        return cls(
            data=items,
            pagination=Pagination(
                page=page_params.page,
                size=page_params.size,
                sort_by=sort_params.sort_by,
                sort_order=sort_params.sort_order,
                total_items=tota_count,
                total_pages=total_pages,
                next_page=(
                    page_params.page + 1
                    if page_params.page < total_pages else None
                ),
                past_page=(
                    page_params.page -1 if page_params.page > 1 else None
                ),
            ),
        )
