from src.fetcher import Fetcher
from src.parser import Parser
from src.database import Database
from src.content_fetcher import ContentFetcher


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
