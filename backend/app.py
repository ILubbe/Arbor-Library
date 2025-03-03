import time
import os
from config import app, db, r
from models import User, Book, Genre, Book_Genre, Reservation, Checkout, SearchableMixin
from routes import users_bp, books_bp, genres_bp, books_genres_bp, reservations_bp, checkouts_bp, login_bp, search_bp
from seed import create_default_admin_user, fetch_and_populate_books
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
                print('Connected to ElasticSearch!')
                db.create_all()
                print('Connected to MariaDB, schema exists!')
                r.ping()
                print('Connected to Redis!')
                # can toggle off seedping by setting BOOTSTRAP env var to FALSE
                seed = os.getenv('SEED', 'TRUE').upper() in ['TRUE', '1']
                if seed:
                    create_default_admin_user()
                    # can set how many books to pull in
                    db_book_count = int(os.getenv('SEED_BOOK_COUNT', 8145))
                    fetch_and_populate_books(db_book_count)
                break
        except Exception as e:
            retries += 1
            print(f"Seed: Waiting for database, redis, and elasticsearch connections. Attmept {retries} of {max_retries}. {e}")
            if retries < max_retries:
                time.sleep(delay)
            else:
                print('Seed: start up failure')
    app.run(host="0.0.0.0", port=5000, debug=True)
