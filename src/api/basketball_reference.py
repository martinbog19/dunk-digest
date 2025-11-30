import httpx
import os
from bs4 import BeautifulSoup
import pandas as pd
from io import StringIO


class BBRefAPI:
    def __init__(self):
        self.base_url = "https://www.basketball-reference.com"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/117.0.0.0 Safari/537.36",
            "Accept-Language": "en-US,en;q=0.9",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        }
        self.timeout = 10.0

    def _open_page(self, endpoint: str) -> httpx.Response:
        url = os.path.join(self.base_url, endpoint)

        with httpx.Client(headers=self.headers, timeout=self.timeout) as client:
            page = client.get(url)
            page.raise_for_status()
            return page

    def get_table(self, endpoint: str) -> pd.DataFrame:
        page = self._open_page(endpoint)
        soup = BeautifulSoup(page.content, "lxml")
        table = soup.find("table")
        stats = pd.read_html(StringIO(str(table)))[0]

        return stats
