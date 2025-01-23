import requests
from flask import Blueprint, request, jsonify
from models import Book_Genre, Book, Genre, db
from utils.general_utils import *

# define blueprint
books_genres_bp = Blueprint('books_genres', __name__, url_prefix='/books-genres')

# read all books_genres
@books_genres_bp.route("/", methods=["GET"], strict_slashes=False)
def get_books_genres():
    books_genres = Book_Genre.query.all()
    json_books_genres = list(map(lambda x: x.book_genre_to_json(), books_genres))
    return jsonify({"booksGenres": json_books_genres}), 200

# read book id(s) by genre-id
@books_genres_bp.route("/books-by-genre/<int:genre_id>", methods=["GET"], strict_slashes=False)
def get_books_by_genre(genre_id):
    # ensure the genre exists
    url = f"http://localhost:5000/genres/{genre_id}"
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException:
        return response.json(), response.status_code

    books_by_genre = Book_Genre.query.filter_by(genre_id=genre_id).all()
    if not books_by_genre:
        return jsonify({"message": "No books associated with this genre"}), 200

    book_ids = [book.book_id for book in books_by_genre]
    
    return jsonify({"booksByGenre": book_ids}), 200

# read genre id(s) by book-id
@books_genres_bp.route("/genres-by-book/<int:book_id>", methods=["GET"], strict_slashes=False)
def get_genres_by_book(book_id):
    # ensure the book exists
    url = f"http://localhost:5000/books/{book_id}"
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException:
        return response.json(), response.status_code

    genres_by_book = Book_Genre.query.filter_by(book_id=book_id).all()
    if not genres_by_book:
        return jsonify({"message": "No genres associated with this book"}), 200

    genre_ids = [genre.genre_id for genre in genres_by_book]

    return jsonify({"GenresByBook": genre_ids}), 200

# associate a book with a genre
@books_genres_bp.route("/associate-book-to-genre", methods=["POST"], strict_slashes=False)
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

    # ensure book and genre actually exist
    url = f"http://localhost:5000/books/{book_id}"
    try:
        response = requests.get(url)
        response.raise_for_status()

        url = f"http://localhost:5000/genres/{genre_id}"
        response = requests.get(url)
        response.raise_for_status()

        # ensure the book isnt already associated to the genre
        url = f"http://localhost:5000/books-genres/genres-by-book/{book_id}"
        response = requests.get(url)
        response.raise_for_status()

    except requests.exceptions.RequestException:
        return response.json(), response.status_code
        
    if genre_id in response.json().get("GenresByBook", []):
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
        return jsonify({"message": "Something went wrong, please try again"}), 400

    return jsonify({"message": f"Book-to-Genre association created!"}), 201


