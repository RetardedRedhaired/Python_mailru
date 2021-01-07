import asyncio
import aiohttp
import time
from sys import stdout

URL = 'https://loremflickr.com/320/240'
tasks = []


def write_to_file(data):
    f = open(f'photo_{time.time()}', 'wb')
    f.write(data)
    f.close()


async def fetch(url, session):
    loop = asyncio.get_event_loop()
    async with session.get(url, allow_redirects=True) as resp:
        data = await resp.read()
        await loop.run_in_executor(None, write_to_file, data)


async def main():
    async with aiohttp.ClientSession() as session:
        for _ in range(10):
            tasks.append(asyncio.create_task(fetch(URL, session)))
        await asyncio.gather(*tasks)


if __name__ == '__main__':
    t1 = time.time()
    asyncio.run(main())
    t2 = time.time()
    print('T', t2 - t1)
