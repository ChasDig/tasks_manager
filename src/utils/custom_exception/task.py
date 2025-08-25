from fastapi import HTTPException, status


class TaskAlreadyExistsError(HTTPException):
    """Ошибка - Активная Задача с таким наименованием уже создана."""

    def __init__(self, detail: str = "Task already exists") -> None:
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail=detail,
        )


class TaskCreateError(HTTPException):
    """Ошибка - ошибка при создании Задачи."""

    def __init__(self, detail: str = "Error create Task") -> None:
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=detail,
        )


class TaskUpdateError(HTTPException):
    """Ошибка - ошибка при обновлении Задачи."""

    def __init__(self, detail: str = "Error update Task") -> None:
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=detail,
        )


class TaskDeleteError(HTTPException):
    """Ошибка - ошибка при удалении Задачи."""

    def __init__(self, detail: str = "Error delete Task") -> None:
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=detail,
        )


class TaskNotFoundError(HTTPException):
    """Ошибка - Задача не найдена."""

    def __init__(self, detail: str = "Task not found") -> None:
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=detail,
        )
