import time
import os
from sqlalchemy.exc import OperationalError
from config import app, db
from models import User, Book, Genre, Book_Genre, Reservation, Checkout
from routes import users_bp, books_bp, genres_bp, books_genres_bp, reservations_bp, checkouts_bp, login_bp
from bootstrap import create_default_admin_user, fetch_and_populate_books
from tasks import scheduler

blueprints = [
    users_bp,
    books_bp,
    genres_bp,
    books_genres_bp,
    reservations_bp,
    checkouts_bp,
    login_bp
]

for bp in blueprints:
    app.register_blueprint(bp)

if __name__ == '__main__':
    # this is to handle a db that hasnt fully started yet
    retries = 0
    max_retries = 5
    delay = 5
    while retries < max_retries:
        try:
            with app.app_context():
                db.create_all()
                # can toggle off bootstrapping by setting DB_BOOTSTRAP env var to FALSE
                db_bootstrap = os.getenv('DB_BOOTSTRAP', 'TRUE').upper() in ['TRUE', '1']
                if db_bootstrap:
                    create_default_admin_user()
                    # can set how many books to pull in
                    db_book_count = int(os.getenv('DB_BOOK_COUNT', 8145))
                    fetch_and_populate_books(db_book_count)
                break
        except OperationalError as e:
            retries += 1
            print(f"Waiting for database to come up. Attmept {retries} of {max_retries}.")
            if retries < max_retries:
                time.sleep(delay)
            else:
                raise e
    app.run(debug=True)