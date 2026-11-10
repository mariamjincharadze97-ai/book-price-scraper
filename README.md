# Book price scraper

A small Python scraper that walks every page of [books.toscrape.com](https://books.toscrape.com) (a public sandbox built for scraping practice) and saves the catalogue to a CSV file.

It is a demo project: the same structure works for any paginated product listing.

## What it does

- Follows the "next" link page by page until the catalogue ends
- Collects title, price, star rating, stock status and product URL
- Retries on network errors and server errors, and waits between requests
- Writes clean UTF-8 CSV that opens directly in Excel or Google Sheets

## Run it

```bash
pip install -r requirements.txt
python scraper.py              # all 50 pages -> books.csv
python scraper.py --pages 3    # first 3 pages only
python scraper.py --out my.csv # custom output file
```

## Sample output

| title | price_gbp | rating | in_stock | url |
|---|---|---|---|---|
| A Light in the Attic | 51.77 | 3 | True | https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html |
| Tipping the Velvet | 53.74 | 1 | True | https://books.toscrape.com/catalogue/tipping-the-velvet_999/index.html |
| Soumission | 50.1 | 1 | True | https://books.toscrape.com/catalogue/soumission_998/index.html |

## Tests

The parser is tested offline against a saved HTML snippet, so the tests need no network:

```bash
pytest
```
