"""Offline tests for the parser: no network needed."""

from scraper import parse_page

PAGE = """
<html><body>
<article class="product_pod">
  <p class="star-rating Three"></p>
  <h3><a href="a-light-in-the-attic_1000/index.html" title="A Light in the Attic">A Light in...</a></h3>
  <p class="price_color">£51.77</p>
  <p class="instock availability">In stock</p>
</article>
<article class="product_pod">
  <p class="star-rating Five"></p>
  <h3><a href="sapiens_996/index.html" title="Sapiens">Sapiens</a></h3>
  <p class="price_color">£54.23</p>
  <p class="availability">Out of stock</p>
</article>
<li class="next"><a href="page-2.html">next</a></li>
</body></html>
"""
URL = "https://books.toscrape.com/catalogue/page-1.html"


def test_parses_every_book_on_the_page():
    rows, _ = parse_page(PAGE, URL)
    assert [row["title"] for row in rows] == ["A Light in the Attic", "Sapiens"]


def test_converts_price_rating_and_stock():
    rows, _ = parse_page(PAGE, URL)
    assert rows[0]["price_gbp"] == 51.77
    assert rows[0]["rating"] == 3
    assert rows[0]["in_stock"] is True
    assert rows[1]["in_stock"] is False


def test_builds_absolute_urls():
    rows, next_url = parse_page(PAGE, URL)
    assert rows[0]["url"] == "https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"
    assert next_url == "https://books.toscrape.com/catalogue/page-2.html"


def test_last_page_has_no_next_url():
    _, next_url = parse_page(PAGE.replace('<li class="next"><a href="page-2.html">next</a></li>', ""), URL)
    assert next_url is None
