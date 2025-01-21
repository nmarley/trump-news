from .events import NewsEvent


class ConsoleNotifier:
    """
    Simple handler that prints events to console
    """

    def handle_content_added(self, event: NewsEvent) -> None:
        print(f"\nNew content added at {event.timestamp}:")
        print(f"Title: {event.item.title}")
        print(f"Link: {event.item.link}")

    def handle_content_processed(self, event: NewsEvent) -> None:
        print(f"\nContent processed at {event.timestamp}:")
        print(f"Title: {event.item.title}")
        if event.metadata:
            print("Metadata:", event.metadata)


class EmailNotifier:
    """
    Email notifier - TBD
    """

    def handle_content_processed(self, event: NewsEvent) -> None:
        # placeholder - implement email sending logic here
        pass
