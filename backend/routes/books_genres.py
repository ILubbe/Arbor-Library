from flask import Blueprint, request, jsonify
from models import Book_Genre, db

# define blueprint
books_genres_bp = Blueprint('books_genres', __name__, url_prefix='/books_genres')

# read all books_genres
@books_genres_bp.route("/", methods=["GET"])
def get_books_genres():
    books_genres = Book_Genre.query.all()
    json_books_genres = list(map(lambda x: x.book_genre_to_json(), books_genres))
    return jsonify({"books_genres": json_books_genres})