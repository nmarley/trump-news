from src.fetcher import Fetcher
from src.parser import Parser
from src.database import Database
from src.content_fetcher import ContentFetcher
from src.events import EventEmitter, NewsEventType
from src.handlers import ConsoleNotifier, EmailNotifier
from src.repository import NewsRepository

"""
This script fetches both the news list and full article content from the White House website.
It checks multiple pages until finding existing content to ensure no articles are missed.
"""


def main():
    # Set up infrastructure
    event_emitter = EventEmitter()
    database = Database()
    repository = NewsRepository(database, event_emitter)

    # Set up handlers
    console_notifier = ConsoleNotifier()
    email_notifier = EmailNotifier()

    event_emitter.on(NewsEventType.CONTENT_ADDED, console_notifier.handle_content_added)
    event_emitter.on(
        NewsEventType.CONTENT_PROCESSED, console_notifier.handle_content_processed
    )
    event_emitter.on(
        NewsEventType.CONTENT_PROCESSED, email_notifier.handle_content_processed
    )

    # Initialize components
    fetcher = Fetcher()
    parser = Parser()
    content_fetcher = ContentFetcher(repository, fetcher, parser)

    # 1. Fetch new articles
    print("\nFetching news articles...")
    total_new_items = content_fetcher.fetch_news_items()
    print(f"\nTotal new items added: {total_new_items}")

    # 2. Get count of articles missing content
    items_missing_content = repository.get_items_without_body()
    total_missing = len(items_missing_content)

    if total_missing == 0:
        print("\nNo articles missing content")
        return

    # 3. Fetch content for articles
    print(f"\nFound {total_missing} article(s) missing content, fetching...")

    updated = content_fetcher.fetch_missing_content(items_missing_content, 30, 60)
    print(f"\nUpdated content for {updated} article(s)")
    print(f"Articles still missing content: {total_missing - updated}")


if __name__ == "__main__":
    main()
