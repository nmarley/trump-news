import time
import random
from typing import Optional
from .fetcher import Fetcher
from .parser import Parser
from .models import NewsItem
from .repository import NewsRepository


class ContentFetcher:
    def __init__(self, repository: NewsRepository, fetcher: Fetcher, parser: Parser):
        self.repository = repository
        self.fetcher = fetcher
        self.parser = parser

    def fetch_news_items(self, max_pages: int = 20) -> int:
        """
        Fetch news items from multiple pages until finding existing content.
        Returns the number of new items added.
        """
        total_new_items = 0

        print("Fetching news articles...")
        for page in range(1, max_pages + 1):
            new_items, found_existing = self._fetch_news_page(page)
            total_new_items += new_items
            print(f"Page {page}: Added {new_items} new items")

            if found_existing and new_items == 0:
                print("Found existing content, no new items to add")
                break

            if new_items == 0 and not found_existing:
                print("No more items found")
                break

        return total_new_items

    def _fetch_news_page(self, page_num: int = 1) -> tuple[int, bool]:
        """Fetch and process a single page of news items."""
        url = (
            f"https://www.whitehouse.gov/news/page/{page_num}/"
            if page_num > 1
            else "https://www.whitehouse.gov/news/"
        )
        html = self.fetcher.fetch_page(url)

        if not html:
            return 0, False

        news_items = self.parser.parse_news_page(html)
        if not news_items:
            return 0, False

        # Store items in database
        new_items = 0
        found_existing = False
        for item in news_items:
            if self.repository.item_exists(item.link):
                found_existing = True
                continue
            if self.repository.add_item(item):
                new_items += 1

        return new_items, found_existing

    def fetch_missing_content(
        self, items: list[NewsItem], min_delay: float = 30.0, max_delay: float = 60.0
    ) -> int:
        """
        Fetch content for the provided items without body text.
        Returns the number of items updated.

        Args:
            items: List of NewsItems that need content fetched
            min_delay: Minimum time to wait between requests (in seconds)
            max_delay: Maximum time to wait between requests (in seconds)
        """
        updated = 0
        total_items = len(items)

        for i, item in enumerate(items, 1):
            content = self._fetch_and_parse_content(item.link)
            if content:
                if self.repository.update_content(item.link, content):
                    updated += 1
                    print(f"Updated content for: {item.title}")

            # Skip delay if this was the last item
            if i < total_items:
                delay = random.uniform(min_delay, max_delay)
                print(f"Waiting {delay:.1f} seconds before next request...")
                time.sleep(delay)

        return updated

    def _fetch_and_parse_content(self, url: str) -> Optional[str]:
        """Fetch and parse content for a single article."""
        html = self.fetcher.fetch_page(url)
        if html:
            return self.parser.parse_article_content(html)
        return None
