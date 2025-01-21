import time
from typing import Optional
from .fetcher import Fetcher
from .parser import Parser
from .database import Database


class ContentFetcher:
    def __init__(self, db: Database, fetcher: Fetcher, parser: Parser):
        self.db = db
        self.fetcher = fetcher
        self.parser = parser

    def fetch_missing_content(self, delay: float = 1.0) -> int:
        """
        Fetch content for all items without body text.
        Returns the number of items updated.

        Args:
            delay: Time to wait between requests (in seconds)
        """
        items = self.db.get_items_without_body()
        updated = 0

        for item in items:
            content = self._fetch_and_parse_content(item.link)
            if content:
                if self.db.update_body(item.link, content):
                    updated += 1
                    print(f"Updated content for: {item.title}")

            # Be nice to the server
            time.sleep(delay)

        return updated

    def _fetch_and_parse_content(self, url: str) -> Optional[str]:
        """Fetch and parse content for a single article."""
        html = self.fetcher.fetch_page(url)
        if html:
            return self.parser.parse_article_content(html)
        return None
