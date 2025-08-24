from contextlib import asynccontextmanager
from typing import Any, AsyncGenerator

from core.app_config import config
from core.app_logger import logger
from core.meta_classes import SingletonMeta
from sqlalchemy.engine import URL
from sqlalchemy.exc import InterfaceError, SQLAlchemyError
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)


class AsyncSessionFactory(metaclass=SingletonMeta):
    """Фабрика создания сессий с Postgres."""

    ERROR_EXC_TYPES = (InterfaceError, SQLAlchemyError)

    def __init__(self, *args: Any, async_engine: AsyncEngine, **kwargs: Any):
        super().__init__(*args, **kwargs)

        self._engine: AsyncEngine = async_engine
        self._session_factory = async_sessionmaker(
            bind=async_engine,
            expire_on_commit=False,
        )

    @asynccontextmanager
    async def context_session(self) -> AsyncGenerator[AsyncSession, None]:
        """
        Асинхронный менеджер контекста по созданию асинхронной сессии к
        Postgres через фабрику async_sessionmaker.

        @rtype session: AsyncGenerator[AsyncSession, None]
        @return session:
        """
        session = self._session_factory()

        try:
            yield session

        except self.ERROR_EXC_TYPES as ex:
            logger.error(f"SQLAlchemy(Postgres) error: {ex}")

            if session:
                await session.rollback()

            raise

        except Exception as ex:
            logger.error(f"Not correct SQLAlchemy(Postgres) error: {ex}")

            if session:
                await session.rollback()

            raise

        finally:
            if session:
                await session.close()


URL_ = URL.create(
    drivername=config.pg_drivername,
    database=config.pg_database,
    username=config.pg_username,
    password=config.pg_password,
    host=config.pg_host,
    port=config.pg_port,
)


def create_sqlalchemy_async_engine(url: str | URL) -> AsyncEngine:
    """
    Создание асинхронного движка для подключения к Postgres.

    @type url: str | URL
    @param url:

    @rtype: AsyncEngine
    @return:
    """
    return create_async_engine(
        url=url,
        echo=config.pg_engine_echo,
        pool_pre_ping=config.pg_engine_pool_pre_ping,
        pool_recycle=config.pg_engine_pool_recycle,
        pool_size=config.pg_engine_pool_size,
        max_overflow=config.pg_engine_max_overflow,
    )


async_engine_ = create_sqlalchemy_async_engine(url=URL_)
pg_session_factory = AsyncSessionFactory(async_engine=async_engine_)


async def get_pg_session() -> AsyncGenerator[AsyncSession, Any]:
    """
    Асинхронный генератор для получения активной сессии с Postgres.
    Применение:
    - Обертка для Dependency в FastAPI (раскрытие асинхронных генераторов,
    аналогия - anext).

    @rtype session: AsyncGenerator[AsyncSession, Any]
    @return session:
    """
    async with pg_session_factory.context_session() as session:
        yield session
