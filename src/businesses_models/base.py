from abc import ABC
from typing import Any


class BaseBusinessModel(ABC):

    @property
    def cls_name(self) -> str:
        return self.__class__.__name__

    async def create(self, *args, **kwargs) -> Any:
        """Создание Сущности."""
        raise NotImplementedError(f"Method not Allowed for {self.cls_name}")

    async def get_by_id(self, *args, **kwargs) -> Any:
        """Получение Сущности по ID."""
        raise NotImplementedError(f"Method not Allowed for {self.cls_name}")

    async def get_list(self, *args, **kwargs) -> Any:
        """Получение списка Сущностей."""
        raise NotImplementedError(f"Method not Allowed for {self.cls_name}")

    async def update(self, *args, **kwargs) -> Any:
        """Обновление Сущности."""
        raise NotImplementedError(f"Method not Allowed for {self.cls_name}")

    async def delete(self, *args, **kwargs) -> Any:
        """Удаление Сущности."""
        raise NotImplementedError(f"Method not Allowed for {self.cls_name}")
