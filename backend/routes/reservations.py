from flask import Blueprint, request, jsonify
from sqlalchemy import func
from models import Reservation, User, Book, db
from utils.general_utils import *

# define blueprint
reservations_bp = Blueprint('reservations', __name__, url_prefix='/reservations')

# get all reservations
@reservations_bp.route("/", methods=["GET"], strict_slashes=False)
def get_reservations():
    reservations = Reservation.query.all()
    json_reservations = list(map(lambda x: x.reservation_to_json(), reservations))
    return jsonify({"reservations": json_reservations})

# get all reservation(s) that one user has made
@reservations_bp.route("/reservations-by-user/<int:user_id>", methods=["GET"], strict_slashes=False)
def get_reservations_by_user(user_id):
    # ensure user exists
    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404

    reservations_by_user = Reservation.query.filter_by(user_id=user_id).all()
    if not reservations_by_user:
        return jsonify({"message": "No reservations associated with this user"}), 404

    reservation_ids = [reservation.id for reservation in reservations_by_user]
    
    return jsonify({"reservationsIdByUser": reservation_ids}), 200

# get all reservation(s) made for one book
@reservations_bp.route("/reservations-by-book/<int:book_id>", methods=["GET"], strict_slashes=False)
def get_reservations_by_book(book_id):
    # ensure book exists
    book = Book.query.get(book_id)
    if not book:
        return jsonify({"message": "Book not found"}), 404

    reservations_by_book = Reservation.query.filter_by(book_id=book_id).all()
    if not reservations_by_book:
        return jsonify({"message": "No reservations associated with this book"}), 404

    reservation_ids = [reservation.id for reservation in reservations_by_book]
    
    return jsonify({"reservationsIdByBook": reservation_ids}), 200

# get all reservation(s) that one user has made for one book
@reservations_bp.route("/<int:user_id>/<int:book_id>", methods=["GET"], strict_slashes=False)
def get_reservations_by_book_and_user(user_id, book_id):
    #ensure user and book exist
    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": f"User not found"}), 404

    book = Book.query.get(book_id)
    if not book:
        return jsonify({"message": f"Book not found"}), 404

    reservations_by_book_and_user = Reservation.query.filter_by(user_id=user_id, book_id=book_id)

    reservation_ids = [reservation.id for reservation in reservations_by_book_and_user]

    return jsonify({"reservationsIdByUserAndBook": reservation_ids}), 200


@reservations_bp.route("/", methods=["POST"], strict_slashes=False)
def create_immediate_reservation():
    required_fields = [
        "userId",
        "bookId"
    ]

    # validation for required fields
    has_all_fields, msg = check_required_fields(required_fields)
    if not has_all_fields:
        return jsonify({
            "message": f"Please fill all required fields: {', '.join(msg)}"
        }), 400

    # convert json keys to valid db columns
    user_id = request.json.get("userId")
    book_id = request.json.get("bookId")

    # ensure an active reservation doesn't already exist for this user & book, ensure the book and user exists
    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": f"User not found"}), 404

    book = Book.query.get(book_id)
    if not book:
        return jsonify({"message": f"Book not found"}), 404

    active_reservation = Reservation.query.filter_by(user_id=user_id, book_id=book_id).filter(Reservation.expires_at > func.now()).first()
    if active_reservation:
        return jsonify({"message": "You have already made an active reservation for this book"}), 400


    # create the new reservation
    new_reservation = Reservation(
        user_id = user_id,
        book_id = book_id
    )

    try:
        db.session.add(new_reservation)
        db.session.commit()
    except Exception as e:
        return jsonify({"message": f"Something went wrong, please try again{str,e }"}), 400

    return jsonify({"message": f"Reservation created!"}), 201