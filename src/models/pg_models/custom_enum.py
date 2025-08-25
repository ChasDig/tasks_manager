import enum

from sqlalchemy.dialects.postgresql import ENUM


class Schemas(enum.Enum):
    """Enum - Postgres схемы."""

    task_manager = "task_manager"


class TaskStatusEnum(enum.Enum):
    """Enum - возможные статусы Задач."""

    create = "create"
    in_process = "in_process"
    completed = "completed"

    @classmethod
    def names(cls) -> list[str]:
        return [en.name for en in cls]

    @classmethod
    def statuses_for_create(cls) -> tuple[str, ...]:
        return (cls.create.value,)

    @classmethod
    def new_statuses_for_update(cls) -> tuple[str, ...]:
        return cls.in_process.value, cls.completed.value

    @classmethod
    def current_statuses_for_update(cls) -> tuple[str, ...]:
        return cls.create.value, cls.in_process.value


task_status_enum = ENUM(
    *TaskStatusEnum.names(),
    name="task_status_enum",
    create_type=True,
)
