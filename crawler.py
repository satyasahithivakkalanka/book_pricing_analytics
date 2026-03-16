import requests
import sqlite3
from bs4 import BeautifulSoup
import re  # for cleaning price text

# Base URL for paginated book list
BASE_URL = "https://books.toscrape.com/catalogue/page-{}.html"

# Words to detect in title for has_positive_word flag
POSITIVE_WORDS = ["best", "love", "amazing", "guide", "success", "perfect", "happy"]


# 1) DATABASE SETUP
def setup_database(db_name="books.db"):
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            price REAL,
            rating INTEGER,
            availability TEXT,
            category TEXT,
            url TEXT UNIQUE,
            title_length INTEGER,
            has_positive_word INTEGER
        );
        """
    )

    conn.commit()
    conn.close()


# 2) HELPER: PARSE RATING FROM CLASS
def parse_rating(tag):
    rating_map = {
        "One": 1,
        "Two": 2,
        "Three": 3,
        "Four": 4,
        "Five": 5,
    }
    if tag is None:
        return None

    classes = tag.get("class", [])  # e.g. ['star-rating', 'Three']
    for c in classes:
        if c in rating_map:
            return rating_map[c]
    return None


# 3) PARSE ALL BOOKS FROM A SINGLE PAGE
def parse_page(html):
    soup = BeautifulSoup(html, "html.parser")
    books = []

    # Each book is inside <article class="product_pod">
    for item in soup.select("article.product_pod"):
        # ---- Title ----
        a_tag = item.select_one("h3 a")
        if not a_tag or not a_tag.has_attr("title"):
            continue
        title = a_tag["title"].strip()

        # ---- Price ----
        price_tag = item.select_one("p.price_color")
        if not price_tag:
            continue
        price_text = price_tag.text.strip()
        # Remove everything except digits and dot, handles weird chars like 'Â'
        clean_price = re.sub(r"[^0-9.]", "", price_text)
        if not clean_price:
            continue
        price = float(clean_price)

        # ---- Rating ----
        rating_tag = item.select_one("p.star-rating")
        rating = parse_rating(rating_tag)

        # ---- Availability ----
        avail_tag = item.select_one("p.instock.availability")
        availability = avail_tag.get_text(strip=True) if avail_tag else ""

        # ---- URL (detail page) ----
        rel_url = a_tag["href"]  # e.g. '../../../sharp-objects_997/index.html'
        rel_url = rel_url.replace("../../../", "")
        url = "https://books.toscrape.com/catalogue/" + rel_url

        # ---- Category (rough from URL path) ----
        # e.g. 'mystery/sharp-objects_997/index.html' -> 'mystery'
        category = None
        parts = rel_url.split("/")
        if len(parts) > 1:
            category = parts[0]

        # ---- Derived fields ----
        title_length = len(title)
        lower_title = title.lower()
        has_positive_word = int(any(word in lower_title for word in POSITIVE_WORDS))

        books.append(
            (
                title,
                price,
                rating,
                availability,
                category,
                url,
                title_length,
                has_positive_word,
            )
        )

    return books


# 4) INSERT MANY BOOKS INTO DATABASE
def insert_books(books, db_name="books.db"):
    if not books:
        return

    conn = sqlite3.connect(db_name)
    cur = conn.cursor()

    cur.executemany(
        """
        INSERT OR IGNORE INTO books
        (title, price, rating, availability, category, url, title_length, has_positive_word)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        books,
    )

    conn.commit()
    conn.close()


# 5) MAIN CRAWLER
def crawl_all_pages(max_pages=50, db_name="books.db"):
    setup_database(db_name)
    total_books = 0

    for page in range(1, max_pages + 1):
        url = BASE_URL.format(page)
        print(f"📄 Fetching page {page}: {url}")

        try:
            res = requests.get(url, timeout=10)
        except Exception as e:
            print(f"⚠️ Error fetching page {page}: {e}")
            break

        if res.status_code != 200:
            print(f"⚠️ Page {page} not found (status {res.status_code}). Stopping.")
            break

        books = parse_page(res.text)
        if not books:
            print("⚠️ No books found on this page. Stopping.")
            break

        insert_books(books, db_name=db_name)
        total_books += len(books)
        print(f"✅ Inserted {len(books)} books from page {page} (total: {total_books})")

    print(f"\n🎉 DONE! Total books scraped and saved: {total_books}")


if __name__ == "__main__":
    crawl_all_pages()
