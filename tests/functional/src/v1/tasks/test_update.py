from typing import Any

import aiohttp
import pytest
from configs import config_t
from sqlalchemy import text


@pytest.mark.parametrize(
    "payload_create, payload_update",
    [
        (
            {
                "title": "Test create",
                "description": "Test create",
                "status": "create",
            },
            {
                "title": "Test update",
                "description": "Test update",
                "status": "in_process",
            },
        ),
    ],
)
@pytest.mark.asyncio
async def test_update_task(
    payload_create,
    payload_update,
    async_pg_session_f,
) -> None:
    """
    Тест: обновление задачи по ID.

    @type payload_create:
    @param payload_create:
    @type payload_update:
    @param payload_update:
    @type async_pg_session_f:
    @param async_pg_session_f:

    @rtype: None
    @return:
    """
    uri_create = "/task_manager/tasks/"
    uri_update = "/task_manager/tasks/{task_id}"

    async with aiohttp.ClientSession() as client_session:
        task_id = None
        url_create = config_t.service_url + uri_create
        url_update = config_t.service_url + uri_update

        try:
            # Create
            async with client_session.post(
                url=url_create,
                json=payload_create,
            ) as resp_c:
                resp_create: dict[str, Any] = await resp_c.json()
                task_id = resp_create.get("id")

                assert resp_c.status == 201

                url_update = url_update.format(task_id=task_id)

            # Update
            async with client_session.patch(
                url=url_update,
                json=payload_update,
            ) as resp_u:
                resp_update: dict[str, Any] = await resp_u.json()

                assert resp_u.status == 200
                assert resp_update.get("id") == resp_create.get("id")
                assert resp_update.get("updated_at") != resp_create.get("updated_at")
                assert resp_update.get("title") == payload_update.get("title")
                assert resp_update.get("description") == payload_update.get(
                    "description"
                )
                assert resp_update.get("status") == payload_update.get("status")

        finally:
            if task_id:
                await async_pg_session_f.execute(
                    text("DELETE FROM task_manager.task WHERE id = :task_id"),
                    {"task_id": task_id},
                )
                await async_pg_session_f.commit()
