from dataclasses import dataclass
from datetime import datetime
from enum import Enum, auto
from typing import Any, Callable, Dict, List
from .models import NewsItem


class NewsEventType(Enum):
    """Enumeration of possible news event types"""

    METADATA_ADDED = auto()
    CONTENT_ADDED = auto()
    CONTENT_PROCESSED = auto()


@dataclass
class NewsEvent:
    type: NewsEventType
    item: NewsItem
    timestamp: datetime = datetime.utcnow()
    metadata: Dict[str, Any] | None = None


class EventEmitter:
    def __init__(self):
        self._handlers: Dict[NewsEventType, List[Callable]] = {}

    def on(
        self, event_type: NewsEventType, handler: Callable[[NewsEvent], None]
    ) -> None:
        """Register a handler for an event type"""
        if event_type not in self._handlers:
            self._handlers[event_type] = []
        self._handlers[event_type].append(handler)

    def emit(self, event: NewsEvent) -> None:
        """Emit an event to all registered handlers"""
        for handler in self._handlers.get(event.type, []):
            try:
                handler(event)
            except Exception as e:
                print(f"Error in event handler: {e}")
