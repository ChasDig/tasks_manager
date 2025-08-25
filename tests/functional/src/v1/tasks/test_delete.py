from typing import Any

import aiohttp
import pytest
from configs import config_t
from sqlalchemy import text


@pytest.mark.parametrize(
    "payload",
    [
        {
            "title": "Test delete",
            "description": "Test delete",
            "status": "create",
        },
    ],
)
@pytest.mark.asyncio
async def test_delete_task(payload, async_pg_session_f) -> None:
    """
    Тест: удаление задачи.

    @type payload:
    @param payload:
    @type async_pg_session_f:
    @param async_pg_session_f:

    @rtype: None
    @return:
    """
    uri_create = "/task_manager/tasks/"
    uri_delete = "/task_manager/tasks/{task_id}"

    async with aiohttp.ClientSession() as client_session:
        task_id = None
        url_create = config_t.service_url + uri_create
        url_delete = config_t.service_url + uri_delete

        try:
            # Create
            async with client_session.post(url_create, json=payload) as resp:
                resp_data: dict[str, Any] = await resp.json()
                task_id = resp_data.get("id")

                assert resp.status == 201
                url_delete = url_delete.format(task_id=task_id)

            # Delete
            async with client_session.delete(url_delete) as resp:
                assert resp.status == 204
                task_id = None

        finally:
            if task_id:
                await async_pg_session_f.execute(
                    text("DELETE FROM task_manager.task WHERE id = :task_id"),
                    {"task_id": task_id},
                )
                await async_pg_session_f.commit()
