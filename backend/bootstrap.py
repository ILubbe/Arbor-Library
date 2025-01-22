import requests, random
from config import db
from models import Book

def fetch_and_populate_books():
    # Check if the database is empty
    if Book.query.count() == 0:
        print("Database is empty, fetching book data from API (This might take a minute)")

        subject = "fiction"
        base_url = "https://openlibrary.org"
        subject_url = f"{base_url}/subjects/{subject}.json"
        conditions = ["new", "good", "fair", "poor", "unknown"]
        
        max_books = 5341
        added_books = 0
        limit = 1000
        offset = 0
        while added_books < max_books:
            if (max_books - added_books) < limit:
                limit = max_books - added_books
                offset += limit
            elif added_books != 0 and added_books % limit == 0:
                offset += limit

            url = f"{subject_url}?limit={limit}&offset={offset}"
                
            print(f"requesting book data from {base_url}...")
            response = requests.get(url)
            data = response.json()
            print("data received!")

            for item in data['works']:
                try:
                    title = item.get('title', 'Unknown Title')
                    author = item['authors'][0]['name'] if item.get('authors') else 'Unknown Author'
                    first_publish_year = item.get('first_publish_year', -1)
                    book_condition = random.choice(conditions)

                    # Add the book to the database
                    book = Book(
                    title = title,
                    author = author,
                    first_publish_year = first_publish_year,
                    book_condition = book_condition
                    )

                    db.session.add(book)
                    added_books += 1
                    if added_books % 100 == 0:
                        db.session.commit()
                        print(f"{added_books} of {max_books} added")
                except Exception as e:
                    continue
        db.session.commit()
        print(f"{added_books} of {max_books} added")
    else:
        print("Books already inside database")
    return

