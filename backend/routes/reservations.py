from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from models import Reservation, User, Book, Checkout, db
from sqlalchemy import func, text, asc, desc
from utils.general_utils import *
from utils.rbac_decorators import *

# define blueprint
reservations_bp = Blueprint('reservations', __name__, url_prefix='/reservations')

# get all reservations
@reservations_bp.route("/", methods=["GET"], strict_slashes=False)
@jwt_required()
@role_required('librarian')
def get_reservations():
    # sort & paginate 
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per-page", 50, type=int)  # default 50
    col = request.args.get("col", "id").replace("-", "_").lower()
    order = request.args.get("order", "asc")

    if not hasattr(Reservation, col):
        return jsonify({"message": f"invalid column to sort by: {col}"}), 400

    sorted_column = getattr(Reservation, col)
    order_by = desc(sorted_column) if order.lower() == "desc" else asc(sorted_column)

    reservations_paginated = Reservation.query.order_by(order_by).paginate(page=page, per_page=per_page, error_out=False)

    return jsonify({
        "reservations": [reservation.serialize() for reservation in reservations_paginated.items],
        "total": reservations_paginated.total,
        "page": reservations_paginated.page,
        "pages": reservations_paginated.pages
    })

# get your own reservation info
@reservations_bp.route("/my", methods=["GET"], strict_slashes=False)
@jwt_required()
def get_my_reservations():
    current_user = get_jwt_identity()
    user = User.query.filter_by(id=current_user).first()
    if not user:
        return jsonify({"message": "User not found"}), 404

    reservations_by_user = Reservation.query.filter_by(user_id=user.id).all()
    if not reservations_by_user:
        return jsonify({"reservations": []}), 200

    json_reservations = list(map(lambda x: x.serialize(), reservations_by_user))
    
    return jsonify({"reservations": json_reservations}), 200


# create a reservation for yourself
@reservations_bp.route("/my", methods=["POST"], strict_slashes=False)
@jwt_required()
def create_my_reservation():
    current_user = get_jwt_identity()
    user = User.query.session.get(User, current_user)
    if not user:
        return jsonify({"message": "User not found"}), 404

    required_fields = [
        "bookId"
    ]

    # validation for required fields
    has_all_fields, msg = check_required_fields(required_fields)
    if not has_all_fields:
        return jsonify({
            "message": f"Please fill all required fields: {', '.join(msg)}"
        }), 400

    # convert json keys to valid db columns
    book_id = request.json.get("bookId")

    book = Book.query.session.get(Book, book_id)
    if not book:
        return jsonify({"message": "Book not found"}), 404

    active_reservation = Reservation.query.filter_by(book_id=book_id, status='active').first()
    if active_reservation:
        return jsonify({"message": "This book is already reserved"}), 409
    
    user_already_made_reservation = Reservation.query.filter_by(book_id=book_id, user_id=user.id, status='waiting').first()
    if user_already_made_reservation:
        return jsonify({"message": "This book is already reserved"}), 409

    active_checkout = Checkout.query.filter_by(book_id=book_id, returned=False).first()
    if active_checkout:
        new_reservation = Reservation(
        user_id = user.id,
        book_id = book_id,
        status = "waiting"
        )

        try:
            db.session.add(new_reservation)
            db.session.commit()
        except Exception as e:
            return jsonify({"message": "Something went wrong, please try again"}), 500

        return jsonify(
            {"message": "This book is currently checked out. Your reservation has been created and placed in a waiting status."}
        ), 201

    # create the new reservation
    new_reservation = Reservation(
        user_id = user.id,
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

# delete (cancel) your own reservation
@reservations_bp.route("/my/<int:reservation_id>", methods=["DELETE"], strict_slashes=False)
@jwt_required()
def cancel_my_reservation(reservation_id):
    current_user = get_jwt_identity()
    user = User.query.session.get(User, current_user)
    if not user:
        return jsonify({"message": "User not found"}), 404

    reservation = Reservation.query.filter_by(user_id=current_user, id=reservation_id).first()

    if not reservation:
        return jsonify({"message": "Reservation not found"}), 404
    try:
        db.session.delete(reservation)
        db.session.commit()
    except Exception as e:
        return jsonify({"message": "Something went wrong, please try again"}), 500

    return jsonify({"message": "Your reservation was deleted successfully"}), 201

# delete (cancel) a reservation by id
@reservations_bp.route("/<int:reservation_id>", methods=["DELETE"], strict_slashes=False)
@jwt_required()
@role_required('librarian')
def delete_reservation(reservation_id):
    reservation = Reservation.query.session.get(Reservation, reservation_id)

    if not reservation:
        return jsonify({"message": "Reservation not found"}), 404
    try:
        db.session.delete(reservation)
        db.session.commit()
    except Exception as e:
        return jsonify({"message": "Something went wrong, please try again"}), 500

    return jsonify({"message": "Reservation deleted successfully"}), 201
