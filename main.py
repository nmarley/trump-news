from src.fetcher import Fetcher
from src.parser import Parser
from src.database import Database
from src.content_fetcher import ContentFetcher

"""
This script fetches both the news list and full article content from the White House website.
It checks multiple pages until finding existing content to ensure no articles are missed.
"""


def main():
    # Initialize components
    db = Database()
    fetcher = Fetcher()
    parser = Parser()
    content_fetcher = ContentFetcher(db, fetcher, parser)

    # 1. Fetch new articles
    print("\nStep 1: Fetching news articles...")
    total_new_items = content_fetcher.fetch_news_items()
    print(f"\nTotal new items added: {total_new_items}")

    # 2. Get count of articles missing content
    items_missing_content = db.get_items_without_body()
    total_missing = len(items_missing_content)

    if total_missing == 0:
        print("\nNo articles missing content")
        return

    # 3. Fetch content for articles
    print(f"\nStep 2: Found {total_missing} articles missing content")
    print("Fetching full content for articles...")

    updated = content_fetcher.fetch_missing_content(items_missing_content, 30, 60)
    print(f"\nUpdated content for {updated} articles")
    print(f"Articles still missing content: {total_missing - updated}")


if __name__ == "__main__":
    main()
