from sqlalchemy import *
from config import db

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.Enum('patron', 'librarian'), nullable=False)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)

    def user_to_json(self):
        return {
            "id": self.id,
            "role": self.role,
            "username": self.username,
            "passwordHash": self.password_hash,
            "firstName": self.first_name,
            "lastName": self.last_name
        }

class Book(db.Model):
    __tablename__ = 'books'

    id = db.Column(db.String(12), primary_key=True) # 12-digit numeric string for barcodes
    title = db.Column(db.String(255), nullable=False)
    author = db.Column(db.String(255), nullable=False)
    isbn = db.Column(db.String(13), nullable=False)
    publish_date = db.Column(db.Date, nullable=False)
    condition = db.Column(db.Enum('New', 'Good', 'Fair', 'Poor'), default='Unkown', nullable=False)

    def book_to_json(self):
        return {
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "isbn": self.isbn,
            "publishDate": self.publish_date,
            "condition": self.condition
        }

class Reservation(db.Model):
    __tablename__ = 'reservations'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    book_id = db.Column(db.String(12), db.ForeignKey('books.id'), nullable=False)
    reserved_at = db.Column(db.DateTime, server_default=func.now(), nullable=False)
    expires_at = db.Column(db.DateTime, nullable=False)

    def reservation_to_json(self):
        return {
            "id": self.id,
            "userID": self.user_id,
            "bookID": self.book_id,
            "reservedAt": self.reserved_at,
            "expiresAt": self.expires_at
        }

class Checkout(db.Model):
    __tablename__ = 'checkouts'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    book_id = db.Column(db.String(12), db.ForeignKey('books.id'), nullable=False)
    checked_out_at = db.Column(db.DateTime, server_default=func.now(), nullable=False)
    due_at = db.Column(db.DateTime, nullable=False)
    returned = db.Column(db.Boolean, default=False, nullable=False)

    def checkout_to_json(self):
        return {
            "id": self.id,
            "userID": self.user_id,
            "bookID": self.book_id,
            "checkoutOutAt": self.checked_out_at,
            "dueAt": self.due_at,
            "returned": self.returned
        }
        