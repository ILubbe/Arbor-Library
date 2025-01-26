from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from sqlalchemy import func, text
from models import Reservation, User, Book, Checkout, db
from utils.general_utils import *

# define blueprint
reservations_bp = Blueprint('reservations', __name__, url_prefix='/reservations')

# get all reservations
@reservations_bp.route("/", methods=["GET"], strict_slashes=False)
@jwt_required()
def get_reservations():
    reservations = Reservation.query.all()
    json_reservations = list(map(lambda x: x.reservation_to_json(), reservations))
    return jsonify({"reservations": json_reservations})

# get reservation by id
@reservations_bp.route("/<int:reservation_id>", methods=["GET"])
@jwt_required()
def get_reservation_by_id(reservation_id):
    reservation = Reservation.query.get(reservation_id)

    if reservation is None:
        return jsonify({"message": "Reservation not found"}), 404
    
    return jsonify({"reservation": reservation.reservation_to_json()})

# get all reservation(s) that one user has made
@reservations_bp.route("/by-user/<int:user_id>", methods=["GET"], strict_slashes=False)
@jwt_required()
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
@reservations_bp.route("/by-book/<int:book_id>", methods=["GET"], strict_slashes=False)
@jwt_required()
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

# get active reservation(s) by user
@reservations_bp.route("/by-user/active/<int:user_id>", methods=["GET"], strict_slashes=False)
@jwt_required()
def get_active_reservations_by_user(user_id):
    # ensure user exists
    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404

    active_reservations_by_user = Reservation.query.filter_by(user_id=user_id).filter(Reservation.expires_at > func.now()).all()
    if not active_reservations_by_user:
        return jsonify({"message": "No active reservations associated with this user"}), 404

    active_reservations_by_user_ids = [reservation.id for reservation in active_reservations_by_user]
    
    return jsonify({"activeReservationsIdByUser": active_reservations_by_user_ids}), 200

# get active reservation(s) by book
@reservations_bp.route("/by-book/active/<int:book_id>", methods=["GET"], strict_slashes=False)
@jwt_required()
def get_active_reservations_by_book(book_id):
    # ensure book exists
    book = Book.query.get(book_id)
    if not book:
        return jsonify({"message": "Book not found"}), 404

    active_reservations_by_book = Reservation.query.filter_by(book_id=book_id).filter(Reservation.expires_at > func.now()).all()
    if not active_reservations_by_book:
        return jsonify({"message": "No active reservations associated with this book"}), 404

    active_reservations_by_book_ids = [reservation.id for reservation in active_reservations_by_book]
    
    return jsonify({"activeReservationsIdByBook": active_reservations_by_book_ids}), 200

# get all reservation(s) that one user has made for one book
@reservations_bp.route("/<int:user_id>/<int:book_id>", methods=["GET"], strict_slashes=False)
@jwt_required()
def get_reservations_by_book_and_user(user_id, book_id):
    #ensure user and book exist
    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404

    book = Book.query.get(book_id)
    if not book:
        return jsonify({"message": "Book not found"}), 404

    reservations_by_book_and_user = Reservation.query.filter_by(user_id=user_id, book_id=book_id)

    reservation_ids = [reservation.id for reservation in reservations_by_book_and_user]

    return jsonify({"reservationsIdByUserAndBook": reservation_ids}), 200

# create a reservation that goes into effect immediately
@reservations_bp.route("/", methods=["POST"], strict_slashes=False)
@jwt_required()
def create_reservation():
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
        return jsonify({"message": "User not found"}), 404

    book = Book.query.get(book_id)
    if not book:
        return jsonify({"message": "Book not found"}), 404

    active_reservation = Reservation.query.filter_by(book_id=book_id, status='active').first()
    if active_reservation:
        return jsonify({"message": "This book is already reserved"}), 400
    
    user_already_made_reservation = Reservation.query.filter_by(book_id=book_id, user_id=user_id, status='waiting').first()
    if user_already_made_reservation:
        return jsonify({"message": "You already have a reservation for this book. You will be notified when the book is returned. If other patrons have this book also reserved, it is first come first serve."}), 400

    active_checkout = Checkout.query.filter_by(book_id=book_id, returned=False).first()
    if active_checkout:
        new_reservation = Reservation(
        user_id = user_id,
        book_id = book_id,
        status = "waiting"
        )

        try:
            db.session.add(new_reservation)
            db.session.commit()
        except Exception as e:
            return jsonify({"message": "Something went wrong, please try again"}), 500

        return jsonify(
            {"message": "This book is currently checked out. You will be notified when the book is returned. Your reservation has been created, however, if other patrons have this book also reserved, it is first come first serve."}
        ), 201

    # create the new reservation
    new_reservation = Reservation(
        user_id = user_id,
        book_id = book_id,
        status = 'active',
        expires_at = text("DATE_ADD(NOW(), INTERVAL 4 DAY)") # reservation expires in 4 days
    )

    try:
        db.session.add(new_reservation)
        db.session.commit()
    except Exception as e:
        return jsonify({"message": "Something went wrong, please try again"}), 500

    return jsonify({"message": "Reservation created!"}), 201

# delete (cancel) a reservation by id
@reservations_bp.route("/<int:reservation_id>", methods=["DELETE"], strict_slashes=False)
@jwt_required()
def delete_reservation(reservation_id):
    reservation = Reservation.query.get(reservation_id)

    if not reservation:
        return jsonify({"message": "Reservation not found"}), 404
    try:
        db.session.delete(reservation)
        db.session.commit()
    except Exception as e:
        return jsonify({"message": "Something went wrong, please try again"}), 500

    return jsonify({"message": "Reservation deleted successfully"}), 200
