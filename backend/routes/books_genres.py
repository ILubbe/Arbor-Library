from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from models import Book_Genre, Book, Genre, db
from utils.general_utils import *

# define blueprint
books_genres_bp = Blueprint('books_genres', __name__, url_prefix='/books-genres')

# read all books_genres
@books_genres_bp.route("/", methods=["GET"], strict_slashes=False)
@jwt_required()
def get_books_genres():
    books_genres = Book_Genre.query.all()
    json_books_genres = list(map(lambda x: x.book_genre_to_json(), books_genres))
    return jsonify({"booksGenres": json_books_genres}), 200

# read book id(s) by genre-id
@books_genres_bp.route("/books-by-genre/<int:genre_id>", methods=["GET"], strict_slashes=False)
@jwt_required()
def get_books_by_genre(genre_id):
    # ensure the genre exists
    genre = Genre.query.get(genre_id)
    if not genre:
        return jsonify({"message": "Genre not found"}), 404

    books_by_genre = Book_Genre.query.filter_by(genre_id=genre_id).all()
    if not books_by_genre:
        return jsonify({"message": "No books associated with this genre"}), 404

    book_ids = [book.book_id for book in books_by_genre]
    
    return jsonify({"booksByGenre": book_ids}), 200

# read genre id(s) by book-id
@books_genres_bp.route("/genres-by-book/<int:book_id>", methods=["GET"], strict_slashes=False)
@jwt_required()
def get_genres_by_book(book_id):
    # ensure the book exists
    book = Book.query.get(book_id)
    if not book:
        return jsonify({"message": "Book not found"}), 404

    genres_by_book = Book_Genre.query.filter_by(book_id=book_id).all()
    if not genres_by_book:
        return jsonify({"message": "No genres associated with this book"}), 404

    genre_ids = [genre.genre_id for genre in genres_by_book]

    return jsonify({"GenresByBook": genre_ids}), 200

# associate a book with a genre
@books_genres_bp.route("/associate-book-to-genre", methods=["POST"], strict_slashes=False)
@jwt_required()
def associate_book_to_genre():
    required_fields = [
        "bookId",
        "genreId"
    ]

    # validation for required fields
    has_all_fields, msg = check_required_fields(required_fields)
    if not has_all_fields:
        return jsonify({
            "message": f"Please fill all required fields: {', '.join(msg)}"
        }), 400

    # convert json keys to valid db columns
    book_id = request.json.get("bookId")
    genre_id = request.json.get("genreId")

    # ensure book and genre actually exist, and book isn't already associated to the genre
    book = Book.query.get(book_id)
    if not book:
        return jsonify({"message": "Book not found"}), 404

    genre = Genre.query.get(genre_id)
    if not genre:
        return jsonify({"message": "Genre not found"}), 404

    # Check if the book is already associated with the genre
    existing_association = Book_Genre.query.filter_by(book_id=book_id, genre_id=genre_id).first()
    if existing_association:
        return jsonify({"message": "Book is already associated with this genre"}), 400


    # create new association
    new_association = Book_Genre(
        book_id = book_id,
        genre_id = genre_id
    )

    # validate length
    length_ok, field = field_length_ok(Book_Genre, new_association)
    if not length_ok:
        field = field.replace("_", " ").title()
        return jsonify({
            "message": f"The following field is too long: {field}"
        }), 400

    try:
        db.session.add(new_association)
        db.session.commit()
    except Exception as e:
        return jsonify({"message": "Something went wrong, please try again"}), 500

    return jsonify({"message": "Book-to-Genre association created!"}), 201

# unassociate a book to a genre by book & genre ids
@books_genres_bp.route("/<int:book_id>/<int:genre_id>", methods=["DELETE"], strict_slashes=False)
@jwt_required()
def delete_book_genre_association(book_id, genre_id):
    book = Book.query.get(book_id)
    if not book:
        return jsonify({"message": "Book not found"}), 404

    genre = Genre.query.get(genre_id)
    if not genre:
        return jsonify({"message": "Genre not found"}), 404

    book_genre = Book_Genre.query.filter_by(book_id=book_id, genre_id=genre_id).first()
    if not book_genre:
        return jsonify({"message": "Book-Genre association not found"}), 404

    try:
        db.session.delete(book_genre)
        db.session.commit()
    except Exception as e:
        return jsonify({"message": "Something went wrong, please try again"}), 500

    return jsonify({"message": "Book-Genre association deleted successfully"}), 200


