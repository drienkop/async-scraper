import asyncio
import logging

import aiohttp
import backoff

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger('async_scraper')


class AsyncScraper:
    def __init__(self, urls, requests_per_second, concurrent_requests, ignore_codes=None, headers=None):
        self.urls = urls
        self.requests_per_second = requests_per_second
        self.concurrent_requests = concurrent_requests
        self.ignore_codes = [] if ignore_codes is None else ignore_codes
        self.headers = headers

        self._loop = asyncio.get_event_loop()
        self._semaphore = asyncio.BoundedSemaphore(self.concurrent_requests)

    async def _fetch_all_urls(self):
        tasks = [self._loop.create_task(self._fetch_url(url)) for url in self.urls]
        results = [self.parse(await t) for t in tasks]
        return results

    @backoff.on_exception(backoff.expo, aiohttp.ClientError, max_tries=20)
    async def _fetch_url(self, url):
        await asyncio.sleep(1 / self.requests_per_second)
        async with self._semaphore:
            logging.info(f'Fetching: {url}')

            async with aiohttp.ClientSession(headers=self.headers) as session:
                async with session.get(url) as response:
                    if response.status not in self.ignore_codes:
                        response.raise_for_status()
                    return await response.text()

    def run(self):
        return self._loop.run_until_complete(self._fetch_all_urls())

    def parse(self, html):
        return html
