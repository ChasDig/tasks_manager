from abc import ABC
from typing import Any


class BaseBusinessModel(ABC):

    @property
    def cls_name(self) -> str:
        return self.__class__.__name__

    async def create(self, *args: Any, **kwargs: Any) -> Any:
        """Создание Сущности."""
        raise NotImplementedError(f"Method not Allowed for {self.cls_name}")

    async def get_by_id(self, *args: Any, **kwargs: Any) -> Any:
        """Получение Сущности по ID."""
        raise NotImplementedError(f"Method not Allowed for {self.cls_name}")

    async def get_list(self, *args: Any, **kwargs: Any) -> Any:
        """Получение списка Сущностей."""
        raise NotImplementedError(f"Method not Allowed for {self.cls_name}")

    async def update(self, *args: Any, **kwargs: Any) -> Any:
        """Обновление Сущности."""
        raise NotImplementedError(f"Method not Allowed for {self.cls_name}")

    async def delete(self, *args: Any, **kwargs: Any) -> Any:
        """Удаление Сущности."""
        raise NotImplementedError(f"Method not Allowed for {self.cls_name}")
