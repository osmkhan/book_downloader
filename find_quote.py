"""
Find a specific quote inside a Google Books volume by running the
built-in "Search inside the book" for several phrasings and printing
the snippets Google returns.

Usage:
    python find_quote.py <book_id> <phrase> [<phrase> ...]

Example:
    python find_quote.py 4v8vAQAAIAAJ "man of the right" "of the right" \
        "I am a man" "right-winger"
"""

import sys
import time
from urllib.parse import quote_plus

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By


SEARCH_URL = "https://books.google.com/books?id={book_id}&q={query}&jtp=1"


def make_driver():
    opts = Options()
    opts.add_argument("--headless=new")
    opts.add_argument("--log-level=3")
    opts.add_experimental_option("excludeSwitches", ["enable-logging"])
    return webdriver.Chrome(options=opts)


def collect_snippets(driver, book_id, phrase, pause=2.0):
    url = SEARCH_URL.format(book_id=book_id, query=quote_plus(f'"{phrase}"'))
    driver.get(url)
    time.sleep(pause)

    hits = []
    for sel in (
        "div.sp_fragment",
        "div.snippet",
        "span.sp_fragment",
        "div.bookcontent",
    ):
        for el in driver.find_elements(By.CSS_SELECTOR, sel):
            text = (el.text or "").strip()
            if text and text not in hits:
                hits.append(text)
    return url, hits


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)

    book_id = sys.argv[1]
    phrases = sys.argv[2:]

    driver = make_driver()
    try:
        for phrase in phrases:
            print(f"\n=== {phrase!r} ===")
            url, hits = collect_snippets(driver, book_id, phrase)
            print(f"  {url}")
            if not hits:
                print("  (no snippets returned)")
                continue
            for h in hits:
                print(f"  - {h}")
    finally:
        driver.quit()


if __name__ == "__main__":
    main()
