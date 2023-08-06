from abc import ABC, abstractmethod

from httpx import URL, AsyncClient


class ICDCrawler(ABC):
    def __init__(self, client: AsyncClient) -> None:
        self.client = client

    @abstractmethod
    async def crawl_suburls(self, url: URL) -> list[URL]:
        ...

    @abstractmethod
    async def crawl_icd(self, url: URL) -> list[str]:
        ...
