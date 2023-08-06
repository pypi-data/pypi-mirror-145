from bs4 import BeautifulSoup
from httpx import URL

from .abstract import ICDCrawler


class ICD9DataComCrawler(ICDCrawler):
    async def crawl_suburls(self, url: URL) -> list[URL]:
        resp = await self.client.get(url)
        last_part = resp.url.path.strip("/default.htm").split("/")[-1]
        if "-" not in last_part:
            return []
        atags = BeautifulSoup(resp.text, "lxml").select(
            "body > div.container-fluid > div > div.col-md-10.contentWrapper ul > li > a.identifier"
        )
        hrefs = [atag.get("href") for atag in atags]
        return [resp.url.copy_with(path=href) for href in hrefs]

    async def crawl_icd(self, url: URL) -> list[str]:
        resp = await self.client.get(url)
        atags = BeautifulSoup(resp.text, "lxml").select(
            "body > div.container-fluid > div > div.col-md-10.contentWrapper > div.codeHierarchyInnerWrapper > ul.codeHierarchyUL > li.hierarchyLine > span.localLine > a[id]"
        )
        return [atag.string for atag in atags]
