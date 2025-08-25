from typing import Any

import aiohttp
import pytest
from configs import config_t
from sqlalchemy import text


@pytest.mark.parametrize(
    "payload",
    [
        {
            "title": "Test create",
            "description": "Test create",
            "status": "create",
        },
    ],
)
@pytest.mark.asyncio
async def test_get_by_id_task(payload, async_pg_session_f) -> None:
    """
    Тест: получение задачи по ID.

    @type payload:
    @param payload:
    @type async_pg_session_f:
    @param async_pg_session_f:

    @rtype: None
    @return:
    """
    uri_create = "/task_manager/tasks/"
    uri_get = "/task_manager/tasks/{task_id}"

    async with aiohttp.ClientSession() as client_session:
        task_id = None
        url_create = config_t.service_url + uri_create
        url_get = config_t.service_url + uri_get

        try:
            # Create
            async with client_session.post(
                url=url_create,
                json=payload,
            ) as resp_c:
                resp_create: dict[str, Any] = await resp_c.json()
                task_id = resp_create.get("id")

                assert resp_c.status == 201

                url_get = url_get.format(task_id=task_id)

            # Get by ID
            async with client_session.get(url=url_get) as resp_g:
                resp_get: dict[str, Any] = await resp_g.json()

                assert resp_g.status == 200
                assert resp_get.get("id") == resp_create.get("id")

        finally:
            if task_id:
                await async_pg_session_f.execute(
                    text("DELETE FROM task_manager.task WHERE id = :task_id"),
                    {"task_id": task_id},
                )
                await async_pg_session_f.commit()
