import time
from sqlalchemy.exc import OperationalError
from config import app, db
from models import User, Book, Genre, Book_Genre, Reservation, Checkout
from routes import users_bp, books_bp, genres_bp, books_genres_bp, reservations_bp, checkouts_bp
from bootstrap import fetch_and_populate_books

blueprints = [
    users_bp,
    books_bp,
    genres_bp,
    books_genres_bp,
    reservations_bp,
    checkouts_bp
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
                fetch_and_populate_books()
                break
        except OperationalError as e:
            retries += 1
            print(f"Waiting for database to come up. Attmept {retries} of {max_retries}.")
            if retries < max_retries:
                time.sleep(delay)
            else:
                raise e
    app.run(debug=True)