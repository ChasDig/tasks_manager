import os

from dotenv import find_dotenv
from pydantic import Field, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict

ENV_PATH = find_dotenv()


class SettingsTest(BaseSettings):
    """Конфигурации сервиса."""

    model_config = SettingsConfigDict(
        env_file=ENV_PATH,
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # Meta
    service_host: str = Field(
        alias="TASK_MANAGER_SERVICE_HOST",
        default="127.0.0.1",
    )
    service_port: int = Field(
        alias="TASK_MANAGER_SERVICE_PORT",
        default=8001,
    )

    @computed_field
    @property
    def service_url(self) -> str:
        return f"http://{self.service_host}:{self.service_port}"

    log_format: str = Field(
        default="%(asctime)s - %(levelname)s - %(message)s",
    )

    # PostgresDB
    pg_drivername: str = Field(
        default="postgresql+asyncpg",
        alias="TASK_MANAGER_POSTGRES_DRIVERNAME",
    )
    pg_database: str = Field(
        default="task_manager_db",
        alias="TASK_MANAGER_POSTGRES_DB",
    )
    pg_username: str = Field(
        default="task_manager_user",
        alias="TASK_MANAGER_POSTGRES_USER",
    )
    pg_password: str = Field(
        alias="TASK_MANAGER_POSTGRES_PASSWORD",
    )
    pg_host: str = Field(default="127.0.0.1", alias="POSTGRES_HOST")
    pg_port: int = Field(default=5432, alias="POSTGRES_PORT")

    pg_engine_echo: bool = Field(
        default=False,
        description="Log level",
        alias="TASK_MANAGER_POSTGRES_ENGINE_ECHO",
    )
    pg_engine_pool_pre_ping: bool = Field(
        default=True,
        description="Check connection to DB before use",
        alias="TASK_MANAGER_POSTGRES_ENGINE_POOL_PRE_PING",
    )
    pg_engine_pool_recycle: int = Field(
        default=3600,
        description="TTL active connection to DB",
        alias="TASK_MANAGER_POSTGRES_ENGINE_POOL_RECYCLE",
    )
    pg_engine_pool_size: int = Field(
        default=10,
        alias="TASK_MANAGER_POSTGRES_ENGINE_POOL_SIZE",
    )
    pg_engine_max_overflow: int = Field(
        default=10,
        description="Pool size over 'TASK_MANAGER_POSTGRES_ENGINE_POOL_SIZE'",
        alias="TASK_MANAGER_POSTGRES_ENGINE_MAX_OVERFLOW",
    )


config_t = SettingsTest()
