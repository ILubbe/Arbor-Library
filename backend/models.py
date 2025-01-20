from sqlalchemy import *
from sqlalchemy.orm import relationship
from sqlalchemy.sql import expression
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

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    author = db.Column(db.String(255), nullable=False)
    isbn = db.Column(db.String(13), nullable=False)
    publish_date = db.Column(db.Date, nullable=False)
    book_condition = db.Column(db.Enum('unknown', 'new', 'good', 'fair', 'poor'), nullable=False)

    genre = db.relationship('Genre', secondary='books_genres', backref=db.backref('books', lazy=True))

    def book_to_json(self):
        return {
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "isbn": self.isbn,
            "publishDate": self.publish_date,
            "bookCondition": self.book_condition
        }

class Genre(db.Model):
    __tablename__ = 'genres'

    id = db.Column(db.Integer, primary_key=True)
    genre = db.Column(db.String(255), unique=True, nullable=False)

    book = db.relationship('Book', secondary='books_genres', backref=db.backref('genres', lazy=True))

    def genre_to_json(self):
        return {
            "id": self.id,
            "genre": self.genre
        }

# Linking table for many-to-many relationship
class Book_Genre(db.Model):
    __tablename__ = 'books_genres'

    book_id = db.Column(db.Integer, db.ForeignKey('books.id'), primary_key=True)
    genre_id = db.Column(db.Integer, db.ForeignKey('genres.id'), primary_key=True)

    def book_genre_to_json(self):
        return {
            "bookID": self.book_id,
            "genreID": self.genre_id
        }

class Reservation(db.Model):
    __tablename__ = 'reservations'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'), nullable=False)
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
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'), nullable=False)
    checked_out_at = db.Column(db.DateTime, server_default=func.now(), nullable=False)
    due_at = db.Column(db.DateTime, nullable=False)
    returned = db.Column(db.Boolean, server_default=expression.false(), nullable=False)

    def checkout_to_json(self):
        return {
            "id": self.id,
            "userID": self.user_id,
            "bookID": self.book_id,
            "checkoutOutAt": self.checked_out_at,
            "dueAt": self.due_at,
            "returned": self.returned
        }
        