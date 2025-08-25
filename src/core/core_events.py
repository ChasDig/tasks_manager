import functools

from fastapi import FastAPI
from sqlalchemy import text

from database import pg_session_factory
from utils.custom_exception.base import StartUpError

from .app_logger import logger


class StartUpEvents:
    """Класс реализующий события, при запуске сервиса."""

    @classmethod
    async def exec(cls) -> None:
        start_up_errors = list()

        for name, method in cls.events.items():
            try:
                await method()
                logger.info(f"StartUp event '{name}' was success...")

            except Exception as ex:
                start_up_errors.append(f"'{name}' - {ex}")

        if start_up_errors:
            error = f"[!]Error StartUp events: {'; '.join(start_up_errors)}"
            raise StartUpError(error)

    @staticmethod
    async def check_postgres() -> None:
        async with pg_session_factory.context_session() as pg_session:
            query = await pg_session.execute(text("SELECT 1;"))
            query.one_or_none()

    events = {
        check_postgres.__name__: check_postgres,
    }


def register_core_events(app: FastAPI) -> None:
    app.add_event_handler(
        "startup",
        functools.partial(StartUpEvents.exec),
    )
