from flask import Blueprint, request, jsonify
from models import Book, db

# define blueprint
books_bp = Blueprint('books', __name__, url_prefix='/books')

# read all books
@books_bp.route("/", methods=["GET"], strict_slashes=False)
def get_books():
    books = Book.query.all()
    json_books = list(map(lambda x: x.book_to_json(), books))
    return jsonify({"books": json_books})