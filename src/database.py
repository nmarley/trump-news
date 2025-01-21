import sqlite3
from datetime import datetime
from .models import NewsItem

class Database:
    def __init__(self, db_path: str = "news.db"):
        self.db_path = db_path
        self._init_db()
    
    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS news_items (
                    link TEXT PRIMARY KEY,
                    title TEXT NOT NULL,
                    timestamp DATETIME NOT NULL,
                    body TEXT,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)
    
    def add_news_item(self, item: NewsItem) -> bool:
        """Add a news item to the database. Returns True if new item was added."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.execute(
                    """
                    INSERT OR IGNORE INTO news_items (link, title, timestamp, body)
                    VALUES (?, ?, ?, ?)
                    """,
                    (item.link, item.title, item.timestamp, item.body)
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
                    UPDATE news_items 
                    SET body = ?, updated_at = CURRENT_TIMESTAMP
                    WHERE link = ?
                    """,
                    (body, link)
                )
                return cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return False 
