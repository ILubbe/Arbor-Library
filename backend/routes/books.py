from flask import Blueprint, request, jsonify
from models import Book, db
from utils.general_utils import *

# define blueprint
books_bp = Blueprint('books', __name__, url_prefix='/books')

# get all books
@books_bp.route("/", methods=["GET"], strict_slashes=False)
def get_books():
    books = Book.query.all()
    json_books = list(map(lambda x: x.book_to_json(), books))
    return jsonify({"books": json_books})

@books_bp.route("/", methods=["POST"], strict_slashes=False)
def create_user():
    required_fields = [
        "title",
        "author",
        "bookCondition"
    ]

    # validatione required fields
    has_all_fields, msg = check_required_fields(required_fields)
    if not has_all_fields:
        return jsonify({
            "message": f"Please fill all required fields: {', '.join(msg)}"
        }), 400

    # convert json keys to valid db columns
    title = request.json.get("title")
    author = request.json.get("author")
    # this one is optional
    if request.json.get("firstPublishYear"):
        first_publish_year = request.json.get("firstPublishYear")
    else:
        first_publish_year = None
    book_condition = request.json.get("bookCondition").lower()

    new_book = Book(
        title = title,
        author = author,
        first_publish_year = first_publish_year,
        book_condition = book_condition
    )

    # validate length
    length_ok, field = field_length_ok(Book, new_book)
    if not length_ok:
        field = field.replace("_", " ").title()
        return jsonify({
            "message": f"The following field is too long: {field}"
        }), 400

    try:
        db.session.add(new_book)
        db.session.commit()
    except Exception as e:
        return jsonify({"message": "Something went wrong, please try again"}), 400

    return jsonify({"message": f"Book {title} added!"}), 201