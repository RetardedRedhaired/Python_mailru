import asyncio
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


async def queue_manager(urls):
    while len(urls) != 0:
        print('TEST')
        task = fetch(, session)
        for task in tasks:
            print('TASKSSSS')
            if task.task_done():
                print('task completed', task)
                tasks.get(task)


async def run_task(tasks, sem):
    while not tasks.empty():
        async with sem:
            task = await tasks.get()
            print('TASK STARTED')
            await asyncio.gather(task)



async def main(n, file_name):
    tasks = asyncio.Queue()
    urls = []
    sem = asyncio.Semaphore(value=n)
    async with aiohttp.ClientSession() as session:
        with open(file_name, 'r') as f:
            for line in f:
                urls.append(line.rstrip('\n'))
        await queue_manager(urls)
        for url in urls:
            await tasks.put(fetch(url, session))
        await run_task(tasks, sem)


if __name__ == '__main__':
    asyncio.run(main(int(sys.argv[1]), sys.argv[2]))
