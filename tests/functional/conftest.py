from typing import AsyncGenerator

import pytest_asyncio
from configs import config_t
from sqlalchemy import engine
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)


@pytest_asyncio.fixture(scope="function")
async def async_pg_session_f() -> AsyncGenerator[AsyncSession, None]:
    pg_url = engine.URL.create(
        drivername=config_t.pg_drivername,
        database=config_t.pg_database,
        username=config_t.pg_username,
        password=config_t.pg_password,
        host=config_t.pg_host,
        port=config_t.pg_port,
    )

    async_engine = create_async_engine(
        url=pg_url,
        echo=config_t.pg_engine_echo,
        pool_pre_ping=config_t.pg_engine_pool_pre_ping,
        pool_recycle=config_t.pg_engine_pool_recycle,
        pool_size=config_t.pg_engine_pool_size,
        max_overflow=config_t.pg_engine_max_overflow,
    )
    async_session_factory = async_sessionmaker(
        bind=async_engine,
        expire_on_commit=False,
    )

    async with async_session_factory() as session:
        yield session
        await async_engine.dispose()
