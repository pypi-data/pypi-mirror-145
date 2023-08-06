import asyncio
from collections.abc import Iterable
from typing import Literal

from httpx import URL, AsyncClient

from ._crawl import allatonce_crawl, recursively_crawl
from ._crawler import ICD9DataComCrawler, ICD10DataComCrawler, ICDSearchIDVTWCrawler
from ._format_utils import format_icd_codes


def icd10data_com(
    url: str,
    sort: bool = True,
    dot: bool = True,
) -> list[str]:
    async def runner() -> list[str]:
        async with AsyncClient() as client:
            icd9_codes: list[str] = []
            await recursively_crawl(icd9_codes, ICD10DataComCrawler(client), URL(url))
        return format_icd_codes(icd9_codes, sort=sort, dot=dot)

    return asyncio.run(runner())


def icd9data_com(
    url: str,
    sort: bool = True,
    dot: bool = True,
) -> list[str]:
    async def runner() -> list[str]:
        async with AsyncClient() as client:
            icd10_codes: list[str] = []
            await recursively_crawl(icd10_codes, ICD9DataComCrawler(client), URL(url))
        return format_icd_codes(icd10_codes, sort=sort, dot=dot)

    return asyncio.run(runner())


def icdsearch_idv_tw(
    queries: Iterable[str],
    trans_to: Literal[10, 9],
    sort: bool = True,
    dot: bool = True,
    duplicates: Literal["drop", "ignore"] = "drop",
) -> list[str]:
    async def runner() -> list[str]:
        cumulative_icd_codes = []
        async with AsyncClient() as client:
            for query in queries:
                icd_codes = await allatonce_crawl(
                    ICDSearchIDVTWCrawler(client, query=query, trans_to=trans_to),
                    URL(""),
                )
                cumulative_icd_codes.extend(icd_codes)
        return format_icd_codes(
            cumulative_icd_codes, sort=sort, dot=dot, duplicates=duplicates
        )

    return asyncio.run(runner())
