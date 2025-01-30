import time
import os
from config import app, db, r
from models import User, Book, Genre, Book_Genre, Reservation, Checkout, SearchableMixin
from routes import users_bp, books_bp, genres_bp, books_genres_bp, reservations_bp, checkouts_bp, login_bp, search_bp
from bootstrap import create_default_admin_user, fetch_and_populate_books
from tasks import scheduler

blueprints = [
    users_bp,
    books_bp,
    genres_bp,
    books_genres_bp,
    reservations_bp,
    checkouts_bp,
    login_bp,
    search_bp
]

for bp in blueprints:
    app.register_blueprint(bp)

if __name__ == '__main__':
    # this is to handle a db that hasnt fully started yet
    retries = 0
    max_retries = 10
    delay = 10
    while retries < max_retries:
        try:
            with app.app_context():
                app.es.ping()
                print('Bootstrap: Connected to ElasticSearch!')
                db.create_all()
                print('Bootstrap: Connected to MariaDB, schema exists!')
                r.ping()
                print('Bootstrap: Connected to Redis!')
                # can toggle off bootstrapping by setting BOOTSTRAP env var to FALSE
                bootstrap = os.getenv('BOOTSTRAP', 'TRUE').upper() in ['TRUE', '1']
                if bootstrap:
                    create_default_admin_user()
                    # can set how many books to pull in
                    db_book_count = int(os.getenv('DB_BOOK_COUNT', 8145))
                    fetch_and_populate_books(db_book_count)
                break
        except:
            retries += 1
            print(f"Bootstrap: Waiting for database, redis, and elasticsearch connections. Attmept {retries} of {max_retries}.")
            if retries < max_retries:
                time.sleep(delay)
            else:
                print('Bootstrap: start up failure')
    app.run(debug=True)