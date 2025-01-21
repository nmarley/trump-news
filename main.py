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
    total_new_items = content_fetcher.fetch_news_items()
    print(f"\nTotal new items added: {total_new_items}")

    # 2. Fetch missing content
    if total_new_items > 0:
        print("\nFetching full content for articles...")
        updated = content_fetcher.fetch_missing_content(30, 60)
        print(f"\nUpdated content for {updated} articles")
    else:
        print("\nNo new articles to fetch content for")


if __name__ == "__main__":
    main()
