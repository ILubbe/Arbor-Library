from sqlalchemy import *
from sqlalchemy.orm import relationship
from sqlalchemy.sql import expression
from datetime import timedelta
from config import db
from search import *

class SearchableMixin(object):
    @classmethod
    def search(cls, expression, page, per_page, field=None):
        ids, total = query_index(cls.__tablename__, expression, page, per_page)
        if total == 0:
            return cls.query.filter_by(id=0), 0
        when = {}
        for i in range(len(ids)):
            when[ids[i]] = i

        query = cls.query.filter(cls.id.in_(ids)).order_by(db.case(when, value=cls.id))
        if hasattr(cls, 'genre'):
            query = query.join(Book_Genre, Book_Genre.book_id == cls.id).join(Genre, Genre.id == Book_Genre.genre_id)

        return cls.query.filter(cls.id.in_(ids)).order_by(
            db.case(when, value=cls.id)), total

    @classmethod
    def search_books_by_genre(cls, genre_name, page, per_page):
        query = db.session.query(cls).join(
            Book_Genre, Book_Genre.book_id == cls.id
        ).join(
            Genre, Genre.id == Book_Genre.genre_id
        ).filter(
            Genre.genre.ilike(f"%{genre_name}")
        )

        query = query.offset((page - 1) * per_page).limit(per_page)
        total = query.count()

        return query.all(), total

    @classmethod
    def before_commit(cls, session):
        session._changes = {
            'add': list(session.new),
            'update': list(session.dirty),
            'delete': list(session.deleted)
        }
    
    @classmethod
    def after_commit(cls, session):
        for obj in session._changes['add']:
            if isinstance(obj, SearchableMixin):
                add_to_index(obj.__tablename__, obj)
        for obj in session._changes['update']:
            if isinstance(obj, SearchableMixin):
                add_to_index(obj.__tablename__, obj)
        for obj in session._changes['delete']:
            if isinstance(obj, SearchableMixin):
                remove_from_index(obj.__tablename__, obj)
        session._changes = None

    @classmethod
    def reindex(cls):
        for obj in cls.query:
            add_to_index(cls.__tablename__, obj)
            
db.event.listen(db.session, 'before_commit', SearchableMixin.before_commit)
db.event.listen(db.session, 'after_commit', SearchableMixin.after_commit)

class User(SearchableMixin, db.Model):
    __tablename__ = 'users'
    __searchable__ = ['role', 'email', 'first_name', 'last_name']

    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.Enum('patron', 'librarian'), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)

    def serialize(self):
        return {
            #"id": self.id,
            "role": self.role,
            "email": self.email,
            #"passwordHash": self.password_hash,
            "firstName": self.first_name,
            "lastName": self.last_name
        }

class Book(SearchableMixin, db.Model):
    __tablename__ = 'books'
    __searchable__ = ['title', 'author', 'first_publish_year', 'book_condition']

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(2000), nullable=False)
    author = db.Column(db.String(2000), nullable=False)
    first_publish_year = db.Column(db.Integer)
    book_condition = db.Column(db.Enum('unknown', 'new', 'good', 'fair', 'poor'), nullable=False)

    genre = db.relationship('Genre', secondary='books_genres', back_populates='book')

    def serialize(self):
        return {
            #"id": self.id,
            "title": self.title,
            "author": self.author,
            "firstPublishYear": self.first_publish_year,
            "bookCondition": self.book_condition,
            "genres": [genre.genre for genre in self.genre]
        }

class Genre(db.Model):
    __tablename__ = 'genres'

    id = db.Column(db.Integer, primary_key=True)
    genre = db.Column(db.String(255), unique=True, nullable=False)

    book = db.relationship('Book', secondary='books_genres', back_populates='genre')

    def serialize(self):
        return {
            #"id": self.id,
            "genre": self.genre
        }

# Linking table for many-to-many relationship
class Book_Genre(db.Model):
    __tablename__ = 'books_genres'

    book_id = db.Column(db.Integer, db.ForeignKey('books.id'), primary_key=True)
    genre_id = db.Column(db.Integer, db.ForeignKey('genres.id'), primary_key=True)

    def serialize(self):
        return {
            "bookId": self.book_id,
            "genreId": self.genre_id
        }

class Reservation(SearchableMixin, db.Model):
    __tablename__ = 'reservations'
    __searchable__ = ['status']

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'), nullable=False)
    status = db.Column(db.Enum('active', 'fulfilled', 'expired', 'waiting'), nullable=False)
    reserved_at = db.Column(db.DateTime, nullable=False, server_default=func.now()) # default - reservation starts now
    expires_at = db.Column(db.DateTime)


    def serialize(self):
        return {
            #"id": self.id,
            "userId": self.user_id,
            "bookId": self.book_id,
            "status": self.status,
            "reservedAt": self.reserved_at,
            "expiresAt": self.expires_at
        }

class Checkout(SearchableMixin, db.Model):
    __tablename__ = 'checkouts'
    __searchable__ = ['returned', 'user_id', 'book_id']

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'), nullable=False)
    checked_out_at = db.Column(db.DateTime, nullable=False, server_default=func.now()) # default - checkout starts now
    due_at = db.Column(db.DateTime, nullable=False, default=text("DATE_ADD(NOW(), INTERVAL 3 WEEK)")) # default - due after 3 weeks later)
    returned = db.Column(db.Boolean, nullable=False, server_default=expression.false())

    def serialize(self):
        return {
            #"id": self.id,
            "userId": self.user_id,
            "bookId": self.book_id,
            "checkoutOutAt": self.checked_out_at,
            "dueAt": self.due_at,
            "returned": self.returned
        }
