from bs4 import BeautifulSoup
from httpx import URL

from .abstract import ICDCrawler


class ICD10DataComCrawler(ICDCrawler):
    async def crawl_suburls(self, url: URL) -> list[URL]:
        resp = await self.client.get(url)
        if resp.url.path.count("-") >= 2:
            return []
        atags = BeautifulSoup(resp.text, "lxml").select(
            "body > div.container.vp > div > div.col-sm-8 > div > ul > li > a"
        )
        hrefs = [atag.get("href") for atag in atags]
        return [resp.url.copy_with(path=href) for href in hrefs]

    async def crawl_icd(self, url: URL) -> list[str]:
        resp = await self.client.get(url)
        atags = BeautifulSoup(resp.text, "lxml").select(
            "a.identifierSpacing.identifier"
        )
        return [atag.string for atag in atags if atag.get("href").startswith(url.path)]
