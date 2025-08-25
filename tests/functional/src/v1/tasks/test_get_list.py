from datetime import datetime, UTC
from typing import Any

import aiohttp
import pytest
from sqlalchemy import text

from configs import config_t


@pytest.mark.parametrize(
    "sql_query_create_tasks, tasks_ids",
    [
        (
            f"""
            INSERT INTO task_manager.task 
            (id, title, description, status, created_at, updated_at)
            VALUES 
            ('bf4a4258-2a24-4d5b-890a-6ca25fe7f763', 'Test1', 'Test 1', 
            'create', '{datetime.now(tz=UTC)}', '{datetime.now(tz=UTC)}'), 
            ('1bfcce92-3c06-44f7-81e6-a1f17b7cf656', 'Test2', 'Test 2', 
            'create', '{datetime.now(tz=UTC)}', '{datetime.now(tz=UTC)}');
            """,
            [
                "bf4a4258-2a24-4d5b-890a-6ca25fe7f763",
                "1bfcce92-3c06-44f7-81e6-a1f17b7cf656",
            ],
        ),
    ],
)
@pytest.mark.asyncio
async def test_get_list(
    sql_query_create_tasks,
    tasks_ids,
    async_pg_session_f,
):
    uri_get_list = "/task_manager/tasks/"

    async with aiohttp.ClientSession() as client_session:
        url_get_list = config_t.service_url + uri_get_list

        try:
            # Create in DB
            await async_pg_session_f.execute(text(sql_query_create_tasks))
            await async_pg_session_f.commit()

            # Get list
            async with client_session.get(url=url_get_list) as resp_g_l:
                resp_get_list: dict[str, Any] = await resp_g_l.json()

                assert resp_g_l.status == 200

                data = resp_get_list.get("data", [])
                pagination = resp_get_list.get("pagination", {})

                assert len(data) == len(tasks_ids)
                assert {t["id"] for t in data} == set(tasks_ids)
                assert pagination.get("total_items") == len(tasks_ids)
                assert pagination.get("total_pages") == 1

        finally:
            if ids := [f"'{t_id}'" for t_id in tasks_ids]:
                await async_pg_session_f.execute(
                    text(
                        f"DELETE FROM task_manager.task WHERE id IN "
                        f"({', '.join(ids)})"
                    ),
                )
                await async_pg_session_f.commit()


@pytest.mark.parametrize(
    "sql_query_create_tasks, tasks_ids",
    [
        (
            f"""
            INSERT INTO task_manager.task 
            (id, title, description, status, created_at, updated_at)
            VALUES 
            ('bf4a4258-2a24-4d5b-890a-6ca25fe7f763', 'Test1', 'Test 1', 
            'create', '{datetime.now(tz=UTC)}', '{datetime.now(tz=UTC)}'), 
            ('1bfcce92-3c06-44f7-81e6-a1f17b7cf656', 'Test2', 'Test 2', 
            'create', '{datetime.now(tz=UTC)}', '{datetime.now(tz=UTC)}');
            """,
            [
                "bf4a4258-2a24-4d5b-890a-6ca25fe7f763",
                "1bfcce92-3c06-44f7-81e6-a1f17b7cf656",
            ],
        ),
    ],
)
@pytest.mark.asyncio
async def test_get_list_with_filter(
    sql_query_create_tasks,
    tasks_ids,
    async_pg_session_f,
):
    uri_get_list_filter = "/task_manager/tasks/?title=Test1"

    async with aiohttp.ClientSession() as client_session:
        url_get_list_filter = config_t.service_url + uri_get_list_filter

        try:
            # Create in DB
            await async_pg_session_f.execute(text(sql_query_create_tasks))
            await async_pg_session_f.commit()

            # Get list with filter
            async with client_session.get(url=url_get_list_filter) as resp_g_l:
                resp_get_list: dict[str, Any] = await resp_g_l.json()

                assert resp_g_l.status == 200

                data = resp_get_list.get("data", [])
                pagination = resp_get_list.get("pagination", {})

                assert len(data) == 1
                assert {t["id"] for t in data} == {
                    "bf4a4258-2a24-4d5b-890a-6ca25fe7f763",
                }
                assert pagination.get("total_items") == 1
                assert pagination.get("total_pages") == 1
                assert data[0].get("id") == (
                    "bf4a4258-2a24-4d5b-890a-6ca25fe7f763"
                )

        finally:
            if ids := [f"'{t_id}'" for t_id in tasks_ids]:
                await async_pg_session_f.execute(
                    text(
                        f"DELETE FROM task_manager.task WHERE id IN "
                        f"({', '.join(ids)})"
                    ),
                )
                await async_pg_session_f.commit()


@pytest.mark.parametrize(
    "sql_query_create_tasks, tasks_ids",
    [
        (
            f"""
            INSERT INTO task_manager.task 
            (id, title, description, status, created_at, updated_at)
            VALUES 
            ('bf4a4258-2a24-4d5b-890a-6ca25fe7f763', 'ATest', 'Test A', 
            'create', '{datetime.now(tz=UTC)}', '{datetime.now(tz=UTC)}'), 
            ('1bfcce92-3c06-44f7-81e6-a1f17b7cf656', 'BTest', 'Test B', 
            'create', '{datetime.now(tz=UTC)}', '{datetime.now(tz=UTC)}');
            """,
            [
                "bf4a4258-2a24-4d5b-890a-6ca25fe7f763",
                "1bfcce92-3c06-44f7-81e6-a1f17b7cf656",
            ],
        ),
    ],
)
@pytest.mark.asyncio
async def test_get_list_with_sort(
    sql_query_create_tasks,
    tasks_ids,
    async_pg_session_f,
):
    uri_get_list_sort = "/task_manager/tasks/?sort_by=title&sort_order=desc"

    async with aiohttp.ClientSession() as client_session:
        url_get_list_sort = config_t.service_url + uri_get_list_sort

        try:
            # Create in DB
            await async_pg_session_f.execute(text(sql_query_create_tasks))
            await async_pg_session_f.commit()

            # Get list with sort
            async with client_session.get(url=url_get_list_sort) as resp_g_l:
                resp_get_list: dict[str, Any] = await resp_g_l.json()

                assert resp_g_l.status == 200

                data = resp_get_list.get("data", [])
                pagination = resp_get_list.get("pagination", {})

                assert len(data) == len(tasks_ids)
                assert [t["title"] for t in data] == ["BTest", "ATest"]
                assert pagination.get("total_items") == len(tasks_ids)
                assert pagination.get("total_pages") == 1

        finally:
            if ids := [f"'{t_id}'" for t_id in tasks_ids]:
                await async_pg_session_f.execute(
                    text(
                        f"DELETE FROM task_manager.task WHERE id IN "
                        f"({', '.join(ids)})"
                    ),
                )
                await async_pg_session_f.commit()


@pytest.mark.parametrize(
    "sql_query_create_tasks, tasks_ids",
    [
        (
            f"""
            INSERT INTO task_manager.task 
            (id, title, description, status, created_at, updated_at)
            VALUES 
            ('bf4a4258-2a24-4d5b-890a-6ca25fe7f763', 'ATest', 'Test A', 
            'create', '{datetime.now(tz=UTC)}', '{datetime.now(tz=UTC)}'), 
            ('1bfcce92-3c06-44f7-81e6-a1f17b7cf656', 'BTest', 'Test B', 
            'create', '{datetime.now(tz=UTC)}', '{datetime.now(tz=UTC)}');
            """,
            [
                "bf4a4258-2a24-4d5b-890a-6ca25fe7f763",
                "1bfcce92-3c06-44f7-81e6-a1f17b7cf656",
            ],
        ),
    ],
)
@pytest.mark.asyncio
async def test_get_list_with_page_params(
    sql_query_create_tasks,
    tasks_ids,
    async_pg_session_f,
):
    uri_get_list_pp = "/task_manager/tasks/?size=1&page=1"

    async with aiohttp.ClientSession() as client_session:
        url_get_list_pp = config_t.service_url + uri_get_list_pp

        try:
            # Create in DB
            await async_pg_session_f.execute(text(sql_query_create_tasks))
            await async_pg_session_f.commit()

            # Get list with page params
            async with client_session.get(url=url_get_list_pp) as resp_g_l:
                resp_get_list: dict[str, Any] = await resp_g_l.json()

                assert resp_g_l.status == 200

                data = resp_get_list.get("data", [])
                pagination = resp_get_list.get("pagination", {})

                assert len(data) == 1
                assert pagination.get("total_items") == 2
                assert pagination.get("total_pages") == 2
                assert pagination.get("next_page") == 2
                assert pagination.get("past_page") is None

        finally:
            if ids := [f"'{t_id}'" for t_id in tasks_ids]:
                await async_pg_session_f.execute(
                    text(
                        f"DELETE FROM task_manager.task WHERE id IN "
                        f"({', '.join(ids)})"
                    ),
                )
                await async_pg_session_f.commit()
