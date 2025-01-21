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

    # Fetch missing content
    updated = content_fetcher.fetch_missing_content(60, 90)
    print(f"Updated content for {updated} articles")


if __name__ == "__main__":
    main()
