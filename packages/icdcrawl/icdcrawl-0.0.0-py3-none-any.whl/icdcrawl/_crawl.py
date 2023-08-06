"""
Crawl ICD codes from certain websites.

Support: 
* icd10data.com
* icd9data.com
* http://icdsearch.idv.tw/TRANS/php/search.php
"""
import asyncio
from itertools import chain

from httpx import URL

from ._crawler import ICDCrawler


async def recursively_crawl(
    icd_codes: list[str], crawler: ICDCrawler, url: URL
) -> None:
    suburls = await crawler.crawl_suburls(url)
    if not suburls:
        icd_codes.extend(await crawler.crawl_icd(url))
    else:
        coros = [recursively_crawl(icd_codes, crawler, suburl) for suburl in suburls]
        tasks = [asyncio.create_task(coro) for coro in coros]
        await asyncio.wait(tasks)


async def allatonce_crawl(crawler: ICDCrawler, url: URL) -> list[str]:
    suburls = await crawler.crawl_suburls(url)
    coros = [crawler.crawl_icd(suburl) for suburl in suburls]
    tasks = [asyncio.create_task(coro) for coro in coros]
    icd_codes_2d = await asyncio.gather(*tasks)
    icd_codes = list(chain.from_iterable(icd_codes_2d))
    return icd_codes
