from src.fetcher import Fetcher
from src.parser import Parser
from src.database import Database
from src.content_fetcher import ContentFetcher

"""
This script fetches the full text content for news items that are missing it in the database.
"""


def main():
    # Initialize components
    db = Database()
    fetcher = Fetcher()
    parser = Parser()
    content_fetcher = ContentFetcher(db, fetcher, parser)

    # Get items that need content
    items_missing_content = db.get_items_without_body()
    total_missing = len(items_missing_content)

    if total_missing == 0:
        print("No articles missing content")
        return

    print(f"Found {total_missing} articles missing content")

    # Fetch missing content
    updated = content_fetcher.fetch_missing_content(items_missing_content, 60, 90)
    print(f"\nUpdated content for {updated} articles")
    print(f"Articles still missing content: {total_missing - updated}")


if __name__ == "__main__":
    main()
