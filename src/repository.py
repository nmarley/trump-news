from .database import Database
from .events import EventEmitter, NewsEvent, NewsEventType
from .models import NewsItem


class NewsRepository:
    """
    Repository pattern - handles both data access and domain events
    """

    def __init__(self, database: Database, event_emitter: EventEmitter):
        self.db = database
        self.event_emitter = event_emitter

    def add_item(self, item: NewsItem) -> bool:
        """Add a news item and emit relevant events"""
        if self.db.add_news_item(item):
            self.event_emitter.emit(
                NewsEvent(type=NewsEventType.METADATA_ADDED, item=item)
            )
            return True
        return False

    def update_content(self, link: str, body: str) -> bool:
        """Update item content and emit relevant events"""
        if self.db.update_body(link, body):
            if item := self.db.get_item_by_link(link):
                self.event_emitter.emit(
                    NewsEvent(type=NewsEventType.CONTENT_ADDED, item=item)
                )
            return True
        return False

    # Delegate other methods to database
    def item_exists(self, link: str) -> bool:
        """Check if an item exists"""
        return self.db.item_exists(link)

    def get_items_without_body(self) -> list[NewsItem]:
        """Get items missing content"""
        return self.db.get_items_without_body()

    def get_item_by_link(self, link: str) -> NewsItem | None:
        """Get item by link"""
        return self.db.get_item_by_link(link)

    # Other methods that need both data access and events...
