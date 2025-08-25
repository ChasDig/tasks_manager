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
async def test_create_task(payload, async_pg_session_f) -> None:
    """
    Тест: создание задачи.

    @type payload:
    @param payload:
    @type async_pg_session_f:
    @param async_pg_session_f:

    @rtype: None
    @return:
    """
    uri = "/task_manager/tasks/"

    async with aiohttp.ClientSession() as client_session:
        url = config_t.service_url + uri

        async with client_session.post(url=url, json=payload) as resp:
            resp_data: dict[str, Any] = await resp.json()

            try:
                assert resp.status == 201

                assert resp_data.get("title") == payload["title"]
                assert resp_data.get("description") == payload["description"]
                assert resp_data.get("status") == payload["status"]

                assert resp_data.get("id") is not None
                assert resp_data.get("created_at") is not None
                assert resp_data.get("updated_at") is not None

            finally:
                if task_id := resp_data.get("id"):
                    await async_pg_session_f.execute(
                        text("DELETE FROM task_manager.task WHERE id = :task_id"),
                        {"task_id": task_id},
                    )
                    await async_pg_session_f.commit()


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
async def test_create_task_error(payload, async_pg_session_f) -> None:
    """
    Тест: ошибка создания задачи.

    @type payload:
    @param payload:
    @type async_pg_session_f:
    @param async_pg_session_f:

    @rtype: None
    @return:
    """
    uri = "/task_manager/tasks/"

    async with aiohttp.ClientSession() as client_session:
        url = config_t.service_url + uri
        task_id = None

        try:
            async with client_session.post(url=url, json=payload) as resp_good:
                response_data: dict[str, Any] = await resp_good.json()
                task_id = response_data.get("id")

                assert resp_good.status == 201

            async with client_session.post(url=url, json=payload) as resp_bad:
                assert resp_bad.status == 409

        finally:
            if task_id:
                await async_pg_session_f.execute(
                    text("DELETE FROM task_manager.task WHERE id = :task_id"),
                    {"task_id": task_id},
                )
                await async_pg_session_f.commit()
