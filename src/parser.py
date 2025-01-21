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

    @staticmethod
    def parse_article_content(html: str) -> str | None:
        """Parse the article content from the HTML."""
        try:
            soup = BeautifulSoup(html, "html.parser")
            # Find the div holding the main content by matching a partial class name
            content = soup.find("div", class_=lambda v: v and "entry-content" in v)
            if content:
                return content.get_text("\n", strip=True)
            return None
        except Exception as e:
            print(f"Error parsing article content: {e}")
            return None
