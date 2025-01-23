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
                h2 = li.find("h2", class_="wp-block-post-title")
                if not h2:
                    continue

                a = h2.find("a")
                title = a.text.strip()
                link = a["href"]
                timestamp = li.find("div", class_="wp-block-post-date").find("time")[
                    "datetime"
                ]
                timestamp = datetime.fromisoformat(timestamp)

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
            content = soup.find("div", class_=lambda v: v and "entry-content" in v)
            if content:
                return content.get_text("\n", strip=True)
            return None
        except Exception as e:
            print(f"Error parsing article content: {e}")
            return None
