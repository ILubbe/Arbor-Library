import requests, random
from config import db
from models import User, Book, Genre, Book_Genre
from utils.password_utils import hash_salt_password

def create_default_admin_user():
    # Check if the users table is empty
    if User.query.count() == 0:
        print(f"Bootstrap: users table in database is empty, creating the default admin user\n")
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
        print("Bootstrap: User(s) already inside database")
    return

def fetch_and_populate_books(max_books):
    # Check if the books table is empty
    if Book.query.count() == 0:
        print(f"Bootstrap: books table in database is empty, fetching data for {max_books} book(s) from API (This might take a minute)\n")

        seed_subjects = [
            "horror",
            "history",
            "cooking",
            "science",
            "sports",
            "romance",
            "love",
            "politics",
            "mystery",
            "fantasy",
            "poetry",
            "travel",
            "comedy",
            "religion",
            "art",
            "youth",
            "philosophy"
        ]

        base_url = "https://openlibrary.org"
        conditions = ["new", "good", "fair", "poor", "unknown"]
        
        # openlibrary.org has a limit of 1000 books per request.
        limit = max_books // len(seed_subjects)
        if limit > 1000:
            limit = 1000

        added_books = 0
        added_books_current = added_books
        count = 0
        laps = 0
        offset = 0
        print(f"requesting book data from {base_url}...\n")
        while added_books < max_books:
            if count == len(seed_subjects):
                count = 0
                laps += 1

            if (max_books - added_books) < limit:
                limit = max_books - added_books

            if added_books != 0 and added_books % limit == 0 and laps > 0:
                offset += limit

            subject_url = f"{base_url}/subjects/{seed_subjects[count]}.json"
            url = f"{subject_url}?limit={limit}&offset={offset}"
            try:
                response = requests.get(url)
                response.raise_for_status()
                data = response.json()
            
            except requests.exceptions.RequestException as e:
                print(f"cannot connect to {url} moving on...")
                continue

            except ValueError as e:
                continue

            for item in data['works']:
                try:
                    title = item.get('title', 'Unknown Title')
                    author = item['authors'][0]['name'] if item.get('authors') else 'Unknown Author'
                    first_publish_year = item.get('first_publish_year', -1)
                    book_condition = random.choice(conditions)
                    book_id = added_books + 1

                    # Add the book to the database session
                    book_object = Book(
                    id = book_id,
                    title = title,
                    author = author,
                    first_publish_year = first_publish_year,
                    book_condition = book_condition
                    )

                    db.session.add(book_object)
                    added_books += 1

                    # add books in batches so the commits aren't too large.
                    if added_books % 100 == 0:
                        db.session.commit()

                except Exception as e:
                    print(f"{str, e}")

            # Add primary genre from every book to the database session
            # if it loops back around to the first genre in the seed_subject array, ensure we don't add them again (has to be unique).
            if laps < 1 and added_books_current < added_books:
                genre = seed_subjects[count]

                genre_object = Genre(
                    id = count + 1,
                    genre = genre
                )

                db.session.add(genre_object)
                db.session.commit()

            
            if added_books_current < added_books:
                # add genre ids and book ids to books_genres linking table
                for i in range(added_books_current + 1, added_books + 1, 1):
                    books_genres_object = Book_Genre(
                        book_id = i,
                        genre_id = count + 1
                    )
                    db.session.add(books_genres_object)

                print(f"{added_books - added_books_current} {seed_subjects[count]} book(s) added")
                db.session.commit()
                added_books_current = added_books
                print(f"{added_books} book(s) of {max_books} added\n")

            count += 1

    else:
        print("Bootstrap: Book(s) already inside database")

    return

