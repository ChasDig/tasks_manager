import enum


class SortEnum(enum.Enum):
    """Enum - базовые параметры сортировки по полю."""

    asc = "asc"
    desc = "desc"

    @classmethod
    def names(cls) -> list[str]:
        return [en.name for en in cls]
