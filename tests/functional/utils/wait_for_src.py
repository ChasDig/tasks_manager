import asyncio

import aiohttp
from aiohttp.client_exceptions import ClientConnectorError
from configs import config_t

from utils.custom_exception import WaiteServiceError


async def wait_for_src(max_count: int = 5) -> None:
    """
    Ожидание подключения к Task Manager Service.

    @type max_count: int
    @param max_count:

    @rtype: None
    @return:
    """
    num = 0
    url = config_t.service_url + "/task_manager/internal/health"

    async with aiohttp.ClientSession() as client_session:
        while num < max_count:
            try:
                async with client_session.get(url=url) as resp:
                    if resp.status == 200:
                        break

            except (ConnectionError, ClientConnectorError):
                pass

            await asyncio.sleep(num + 2)
            num += 0.5

        else:
            raise WaiteServiceError()


if __name__ == "__main__":
    asyncio.run(wait_for_src())
