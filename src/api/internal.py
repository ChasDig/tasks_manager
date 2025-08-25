from datetime import datetime, UTC

from fastapi import APIRouter, status

from core.app_config import config


router = APIRouter(
    prefix="/internal",
    tags=["internal"],
)


@router.get("/health", status_code=status.HTTP_200_OK)
async def healthcheck() -> dict[str, str | datetime]:
    """
    Проверка состояния сервиса.

    @rtype: dict[str, str | datetime]
    @return:
    """
    return {
        "status": "ok",
        "timestamp": datetime.now(tz=UTC).isoformat(),
        "service": config.service_name,
    }
