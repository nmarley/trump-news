# Trump news - WhiteHouse.gov news scraper

A Python application that scrapes news articles from whitehouse.gov, storing
both article metadata and full content in a SQLite database, so you can search
it or whatever else you wanna do.

Use this as a starter project for your own Trump news needs. Wrap it in a
FastAPI or Flask service. Add a web frontend. The sky's the limit!

## Features

- Scrapes White House news article metadata (title, link, timestamp)
- Downloads full article content with configurable delays
- Stores everything in a SQLite database
- Handles rate limiting through random delays
- User-agent spoofing for reliable scraping

## Requirements

- Python 3.10+
- Required packages are listed in `requirements.txt`

## Install

```bash
python3 -mvenv ./.venv
./.venv/bin/pip install -r requirements.txt
```

## Format / Lint Check

```bash
./.venv/bin/ruff  format
15 files left unchanged

./.venv/bin/ruff  check
All checks passed!
```

## Usage

Run the script to fetch news and content:

```bash
./.venv/bin/python main.py
```

The script will:
1. Fetch the list of new article metadata
2. Download full content for any new articles
3. Use reasonable delays between requests to avoid rate limiting

The data is stored in `news.db` (SQLite database).

## License

This project is licensed under either of

 * MIT license ([LICENSE-MIT](LICENSE-MIT) or
   https://opensource.org/licenses/MIT)
 * Apache License, Version 2.0, ([LICENSE-APACHE](LICENSE-APACHE) or
   https://www.apache.org/licenses/LICENSE-2.0)
