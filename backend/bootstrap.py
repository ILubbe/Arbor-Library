import requests, random
from config import db
from models import User, Book, Genre, Book_Genre
from utils.password_utils import hash_salt_password

def create_default_admin_user():
    # Check if the users table is empty
    if User.query.count() == 0:
        print(f"Bootstrap: users table in database is empty, creating the default admin user")
        default_admin = User(
            role = 'librarian',
            email = 'defaultadmin@arborlibrary.com',
            password_hash = hash_salt_password('admin'),
            first_name = 'default',
            last_name = 'admin',
        )

        db.session.add(default_admin)
        db.session.commit()

    else:
        print("Bootstrap: Users already inside database")
    return

def fetch_and_populate_books(max_books):
    # Check if the books table is empty
    if Book.query.count() == 0:
        print(f"Bootstrap: books table in database is empty, fetching data for {max_books} book(s) from API (This might take a minute)")

        subject = "fiction"
        base_url = "https://openlibrary.org"
        subject_url = f"{base_url}/subjects/{subject}.json"
        conditions = ["new", "good", "fair", "poor", "unknown"]
        
        added_books = 0
        # openlibrary.org has a limit of 1000 books per request.
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

                    # Add the book to the database session
                    book = Book(
                    title = title,
                    author = author,
                    first_publish_year = first_publish_year,
                    book_condition = book_condition
                    )

                    db.session.add(book)
                    added_books += 1

                    # write books in batches to limit i/o operations.
                    if added_books % 100 == 0:
                        db.session.commit()
                        print(f"{added_books} of {max_books} added")

                except Exception as e:
                    continue

        db.session.commit()
        print(f"{added_books} of {max_books} added")

    else:
        print("Bootstrap: Books already inside database")

    return

