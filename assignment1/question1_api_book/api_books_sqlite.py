import sqlite3
import requests
from pathlib import Path

# keeping the database in the same folder
DB_PATH = Path(__file__).parent / "books.db"

# fetching book data from API
def fetch_books():
    resp = requests.get("https://openlibrary.org/search.json?q=python")

    if resp.status_code != 200:
        print("API call failed, status:", resp.status_code)
        return []

    docs = resp.json().get("docs", [])
    books = []
     # only taking first 13 books for this assignment
    for b in docs[:13]:
        title = b.get("title", "Unknown")
        # author comes as a list, so taking the first one
        author = b["author_name"][0] if b.get("author_name") else "Unknown"
        year = b.get("first_publish_year", "N/A")
        books.append((title, author, year))

    return books

#  creating database and table if not already there
def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS books (
            id    INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            author TEXT,
            publication_year INTEGER
        )
    """)

    conn.commit()
    return conn

# saving books into SQLite
def save_books(conn, books):
    cur = conn.cursor()
    
     # removing old data so duplicates don't duplicate 
    cur.execute("DELETE FROM books")
    
    cur.executemany(
        "INSERT INTO books (title, author, publication_year) VALUES (?, ?, ?)",
        books
    )
    conn.commit()

# showing what's stored in the database
def show_books(conn):
    cur = conn.cursor()
    cur.execute("SELECT title, author, publication_year FROM books")
    rows = cur.fetchall()

    print(f"\nFound {len(rows)} books in the DB:\n")
    for row in rows:
        print(
            f"Title: {row[0]}"
            f"\nAuthor: {row[1]}"
            f"\nYear: {row[2]}"
        )
        print("-" * 50)

# main code starts here
if __name__ == "__main__":
    print("Hitting the Open Library API...")

    books = fetch_books()
    if not books:
        print("Nothing to store, exiting.")
        exit()

    conn = init_db()
    save_books(conn, books)
    show_books(conn)
    conn.close()

    print("\nData successfully stored in SQLite!")