from backend.config import app, db
from backend.models import User, Book, Reservation, Checkout
from backend.routes import users_bp, books_bp, genres_bp, books_genres_bp, reservations_bp, checkouts_bp

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