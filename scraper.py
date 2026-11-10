"""Scrape every book from books.toscrape.com into a CSV file.

books.toscrape.com is a public sandbox built for scraping practice,
so this script is safe to run as-is.

Usage:
    python scraper.py                  # all pages -> books.csv
    python scraper.py --pages 3        # first 3 pages only
    python scraper.py --out data.csv   # custom output file
"""

import argparse
import csv
import sys
import time
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

START_URL = "https://books.toscrape.com/catalogue/page-1.html"
RATINGS = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}
FIELDS = ["title", "price_gbp", "rating", "in_stock", "url"]


def fetch(session, url, retries=3):
    """GET a page, retrying on network errors and 5xx responses."""
    for attempt in range(1, retries + 1):
        try:
            response = session.get(url, timeout=15)
            if response.status_code < 500:
                response.raise_for_status()
                response.encoding = "utf-8"
                return response.text
        except requests.RequestException as error:
            if attempt == retries:
                raise
            print(f"  retry {attempt}/{retries} after error: {error}", file=sys.stderr)
        time.sleep(2 * attempt)
    raise RuntimeError(f"Server kept failing for {url}")


def parse_page(html, page_url):
    """Return (rows, next_page_url) for one catalogue page."""
    soup = BeautifulSoup(html, "html.parser")
    rows = []
    for card in soup.select("article.product_pod"):
        link = card.select_one("h3 a")
        rating_word = card.select_one("p.star-rating")["class"][1]
        rows.append(
            {
                "title": link["title"],
                "price_gbp": float(card.select_one(".price_color").text.lstrip("£")),
                "rating": RATINGS.get(rating_word, 0),
                "in_stock": "In stock" in card.select_one(".availability").text,
                "url": urljoin(page_url, link["href"]),
            }
        )
    next_link = soup.select_one("li.next a")
    next_url = urljoin(page_url, next_link["href"]) if next_link else None
    return rows, next_url


def scrape(max_pages=None, delay=0.5):
    """Walk the catalogue page by page and collect every book."""
    session = requests.Session()
    session.headers["User-Agent"] = "book-price-scraper/1.0 (demo project)"
    url, page, books = START_URL, 0, []
    while url and (max_pages is None or page < max_pages):
        page += 1
        rows, url = parse_page(fetch(session, url), url)
        books.extend(rows)
        print(f"page {page}: {len(rows)} books (total {len(books)})")
        time.sleep(delay)  # be polite to the server
    return books


def save_csv(books, path):
    with open(path, "w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(books)


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--pages", type=int, default=None, help="limit the number of pages")
    parser.add_argument("--out", default="books.csv", help="output CSV path")
    args = parser.parse_args()

    books = scrape(max_pages=args.pages)
    save_csv(books, args.out)
    print(f"Saved {len(books)} books to {args.out}")


if __name__ == "__main__":
    main()
