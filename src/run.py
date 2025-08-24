from fastapi import FastAPI

from api.v1 import tasks_router
from core.app_config import config
from core.core_events import register_core_events

app = FastAPI(
    title=config.service_name,
    description="Service for CRUD options for tasks manager",
    version="0.1.0",
)
app.include_router(tasks_router)
register_core_events(app)
