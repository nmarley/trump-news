from src.fetcher import Fetcher
from src.parser import Parser
from src.database import Database

"""
This script fetches the main news page from the White House website, parses the
news items, and stores them in a database.

Another script will be used to fetch, parse and store the full text of each
news item.
"""


def main():
    # Initialize components
    fetcher = Fetcher()
    parser = Parser()
    db = Database()

    # Fetch and parse the main news page
    url = "https://www.whitehouse.gov/news/"
    html = fetcher.fetch_page(url)

    if html:
        # Parse the news items
        news_items = parser.parse_news_page(html)

        # Store items in database
        new_items = 0
        for item in news_items:
            if db.add_news_item(item):
                new_items += 1

        print(f"Added {new_items} new items to the database")
    else:
        print("Failed to fetch news page")


if __name__ == "__main__":
    main()
