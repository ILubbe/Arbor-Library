from config import app, db
from models import User, Book, Reservation, Checkout
from routes import users_bp, books_bp, genres_bp, books_genres_bp, reservations_bp, checkouts_bp

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
    with app.app_context():
        db.create_all()
    app.run(debug=True)