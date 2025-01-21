import sqlite3
from .models import NewsItem
from datetime import datetime


class Database:
    def __init__(self, db_path: str = "news.db"):
        self.db_path = db_path
        self._init_db()
        self._migrate_db()

    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                create table if not exists news_items (
                    id integer primary key autoincrement,
                    link text unique not null,
                    title text not null,
                    timestamp datetime not null,
                    body text,
                    created_at datetime default current_timestamp,
                    updated_at datetime default current_timestamp
                )
            """)

    def _migrate_db(self):
        """Handle database migrations."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                # Check if id column exists
                cursor = conn.execute("pragma table_info(news_items)")
                columns = [col[1] for col in cursor.fetchall()]

                if "id" not in columns:
                    print("Migrating database to add id column...")
                    # Create new table with desired schema
                    conn.execute("""
                        create table news_items_new (
                            id integer primary key autoincrement,
                            link text unique not null,
                            title text not null,
                            timestamp datetime not null,
                            body text,
                            created_at datetime default current_timestamp,
                            updated_at datetime default current_timestamp
                        )
                    """)

                    # Copy data from old table to new table
                    conn.execute("""
                        insert into news_items_new (link, title, timestamp, body, created_at, updated_at)
                        select link, title, timestamp, body, created_at, updated_at
                        from news_items
                    """)

                    # Drop old table and rename new table
                    conn.execute("drop table news_items")
                    conn.execute("alter table news_items_new rename to news_items")

                    print("Database migration completed successfully")
        except sqlite3.Error as e:
            print(f"Migration error: {e}")

    def add_news_item(self, item: NewsItem) -> bool:
        """Add a news item to the database. Returns True if new item was added."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.execute(
                    """
                    insert or ignore into news_items (link, title, timestamp, body)
                    values (?, ?, ?, ?)
                    returning id
                    """,
                    (item.link, item.title, item.timestamp, item.body),
                )
                if row := cursor.fetchone():
                    item.id = row[0]  # Set the ID on the item
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

    def get_items_without_body(self) -> list[NewsItem]:
        """Get all news items that don't have body content."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.execute(
                    """
                    select id, link, title, timestamp, body
                    from news_items
                    where body is null
                    order by timestamp asc
                    """
                )
                return [
                    NewsItem(
                        id=row["id"],
                        title=row["title"],
                        link=row["link"],
                        timestamp=datetime.fromisoformat(row["timestamp"]),
                        body=row["body"],
                    )
                    for row in cursor.fetchall()
                ]
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return []

    def item_exists(self, link: str) -> bool:
        """Check if an item with the given link already exists."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("select 1 from news_items where link = ?", (link,))
            return cursor.fetchone() is not None
