from dataclasses import dataclass
from datetime import datetime


@dataclass
class NewsItem:
    title: str
    link: str
    timestamp: datetime
    id: int | None = None
    body: str | None = None
