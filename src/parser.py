from bs4 import BeautifulSoup
from datetime import datetime
from typing import List
from .models import NewsItem


class Parser:
    @staticmethod
    def parse_news_page(html: str) -> List[NewsItem]:
        """Parse the news page HTML and return a list of NewsItems."""
        soup = BeautifulSoup(html, "html.parser")
        items = []

        for li in soup.find_all("li", class_="wp-block-post"):
            try:
                a = li.find("h2").find("a")
                title = a.text.strip()
                link = a["href"]
                timestamp = li.find("time")["datetime"]
                timestamp = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))

                items.append(NewsItem(title=title, link=link, timestamp=timestamp))
            except (AttributeError, KeyError) as e:
                print(f"Error parsing news item: {e}")
                continue

        return items
