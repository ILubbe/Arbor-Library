from config import app, db
from models import User, Book, Reservation, Checkout
from routes import users_bp, books_bp#, reservations_bp, checkouts_bp

app.register_blueprint(users_bp)
app.register_blueprint(books_bp)
#app.register_blueprint(reservations_bp)
#app.register_blueprint(checkouts_bp)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)