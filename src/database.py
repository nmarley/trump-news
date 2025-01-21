import sqlite3
from .models import NewsItem


class Database:
    def __init__(self, db_path: str = "news.db"):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                create table if not exists news_items (
                    link text primary key,
                    title text not null,
                    timestamp datetime not null,
                    body text,
                    created_at datetime default current_timestamp,
                    updated_at datetime default current_timestamp
                )
            """)

    def add_news_item(self, item: NewsItem) -> bool:
        """Add a news item to the database. Returns True if new item was added."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.execute(
                    """
                    insert or ignore into news_items (link, title, timestamp, body)
                    values (?, ?, ?, ?)
                    """,
                    (item.link, item.title, item.timestamp, item.body),
                )
                return cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return False

    def update_body(self, link: str, body: str) -> bool:
        """Update the body text for a news item."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.execute(
                    """
                    update news_items 
                    set body = ?, updated_at = current_timestamp
                    where link = ?
                    """,
                    (body, link),
                )
                return cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return False
