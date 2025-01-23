from pathlib import Path
from src.parser import Parser
from datetime import datetime
from zoneinfo import ZoneInfo


def test_parse_news_page():
    """Test that the parser correctly extracts news items from HTML."""
    html = """
    <li class="wp-block-post">
        <div class="wp-block-whitehouse-post-template">
            <div class="wp-block-whitehouse-post-template__content">
                <h2 class="wp-block-post-title">
                    <a href="https://www.whitehouse.gov/briefings-statements/2025/01/test-article/">Test Article</a>
                </h2>
                <div class="wp-block-post-date">
                    <time datetime="2025-01-23T16:42:29-05:00">January 23, 2025</time>
                </div>
            </div>
        </div>
    </li>
    """

    # Wrap in parent element
    html = f'<ul class="wp-block-post-template">{html}</ul>'

    parser = Parser()
    items = parser.parse_news_page(html)

    assert len(items) == 1
    item = items[0]

    assert item.title == "Test Article"
    assert (
        item.link
        == "https://www.whitehouse.gov/briefings-statements/2025/01/test-article/"
    )
    assert item.timestamp == datetime(
        2025, 1, 23, 16, 42, 29, tzinfo=ZoneInfo("America/New_York")
    )


def test_parse_news_page_no_items():
    """Test that parser handles HTML with no news items."""
    html = "<ul class='wp-block-post-template'></ul>"
    parser = Parser()
    items = parser.parse_news_page(html)
    assert len(items) == 0


def test_parse_news_page_invalid_html():
    """Test that parser handles invalid HTML gracefully."""
    html = "<not>valid</html>"
    parser = Parser()
    items = parser.parse_news_page(html)
    assert len(items) == 0


def test_parse_full_news_page():
    """Test parsing a complete news page with multiple entries."""
    # Read the test HTML file
    html_path = Path(__file__).parent / "fixtures" / "whnews.html"
    with open(html_path) as f:
        html = f.read()

    parser = Parser()
    items = parser.parse_news_page(html)

    # Test we got all expected items
    assert len(items) == 9

    # Test first article
    assert items[0].title == (
        "Fact Sheet: President Donald J. Trump Takes Action to Enhance America’s AI Leadership"
    )
    assert items[0].link == (
        "https://www.whitehouse.gov/briefings-statements/2025/01/fact-sheet-president-donald-j-trump-takes-action-to-enhance-americas-ai-leadership/"
    )
    assert items[0].timestamp == datetime(
        2025, 1, 23, 16, 51, 40, tzinfo=ZoneInfo("America/New_York")
    )

    # Test second article
    assert items[1].title == (
        "Fact Sheet: Executive Order to Establish United States Leadership in Digital Financial Technology"
    )
    assert items[1].link == (
        "https://www.whitehouse.gov/briefings-statements/2025/01/fact-sheet-executive-order-to-establish-united-states-leadership-in-digital-financial-technology/"
    )
    assert items[1].timestamp == datetime(
        2025, 1, 23, 16, 42, 29, tzinfo=ZoneInfo("America/New_York")
    )
