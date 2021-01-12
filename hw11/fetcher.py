import asyncio
from queue import Queue

import aiohttp
import sys
import bs4
from collections import Counter
import json

N = 5


def site_parser(data):
    words = Counter()
    soup = bs4.BeautifulSoup(data, 'lxml')
    raw = soup.get_text().replace('\n', ' ').split(' ')
    for s in raw:
        if s.isalpha():
            words[s] += 1
    top_n_words = dict(words.most_common(N))
    return json.dumps(top_n_words)


async def fetch(url, session):
    async with session.get(url, allow_redirects=True) as resp:
        data = await resp.read()
    print(site_parser(data.decode('utf-8')))
    print('task completed')


async def master(urls, tasks, session):
    task_queue = Queue()
    for url in urls:
        task_queue.put(fetch(url, session))
    while not task_queue.empty():
        await tasks.put(task_queue.get())


async def worker(tasks, sem):
    async with sem:
        while not tasks.empty():
            task = await tasks.get()
            print(f"TASK {task} STARTED")
            await asyncio.create_task(task)


async def main(n, file_name):
    tasks = asyncio.Queue()
    urls = []
    sem = asyncio.Semaphore(value=n+1)
    async with aiohttp.ClientSession() as session:
        with open(file_name, 'r') as f:
            for line in f:
                urls.append(line.rstrip('\n'))
        workers = (worker(tasks, sem) for i in range(n))
        await asyncio.gather(master(urls, tasks, session), *workers)


if __name__ == '__main__':
    asyncio.run(main(int(sys.argv[1]), sys.argv[2]))
