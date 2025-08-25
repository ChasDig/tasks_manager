import asyncio
import aiohttp

from configs import config_t
from utils.custom_exception import WaiteServiceError


async def wait_for_src(max_count: int = 5) -> None:
    num = 0
    url = config_t.service_url + "/task_manager/internal/health"

    async with aiohttp.ClientSession() as client_session:
        while num < max_count:
            async with client_session.get(url=url) as resp:
                if resp.status == 200:
                    break

                await asyncio.sleep(num + 1)
                num += 1

        else:
            raise WaiteServiceError()


if __name__ == '__main__':
    asyncio.run(wait_for_src())
