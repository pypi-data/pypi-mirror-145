import re
from math import ceil
from typing import Literal

import pandas as pd
from httpx import URL, Cookies

from .abstract import ICDCrawler


class ICDSearchIDVTWCrawler(ICDCrawler):
    _url = URL("http://icdsearch.idv.tw/TRANS/php/search.php")
    _cookies: Cookies

    def __init__(self, *args, query: str, trans_to: Literal[9, 10], **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.query = query
        self.version = trans_to

    async def crawl_suburls(self, url: URL) -> list[URL]:
        resp = await self.client.get(self._url)
        self._cookies = resp.cookies

        resp = await self.client.post(
            self._url,
            data={"Name": self.query, "Search": "查詢"},
            cookies=self._cookies,
            follow_redirects=True,
        )
        nrecords = int(re.search(r"記錄總數: (\d+) 筆", resp.text).group(1))  # type: ignore
        npages = ceil(nrecords / 20)
        path = "/TRANS/php/contacts.php"
        return [
            self._url.copy_with(path=path, query=f"Pages={page}".encode())
            for page in range(1, npages + 1)
        ]

    async def crawl_icd(self, url: URL) -> list[str]:
        resp = await self.client.post(url, cookies=self._cookies)
        df = pd.read_html(resp.text, header=0)[0]
        col = f"ICD{self.version}編碼"
        return df[col].astype(str).tolist()
