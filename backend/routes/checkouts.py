from datetime import datetime, timedelta
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from models import Checkout, User, Book, Reservation, db
from sqlalchemy import func, asc, desc
from utils.general_utils import *
from utils.rbac_decorators import *

# define blueprint
checkouts_bp = Blueprint('checkouts', __name__, url_prefix='/api/checkouts')

# get all checkouts
@checkouts_bp.route("/", methods=["GET"], strict_slashes=False)
@jwt_required()
@role_required('librarian')
def get_checkouts():
    # sort & paginate 
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per-page", 50, type=int)  # default 50
    col = request.args.get("col", "id").replace("-", "_").lower()
    order = request.args.get("order", "asc")

    if not hasattr(Checkout, col):
        return jsonify({"message": f"invalid column to sort by: {col}"}), 400

    sorted_column = getattr(Checkout, col)
    order_by = desc(sorted_column) if order.lower() == "desc" else asc(sorted_column)

    checkouts_paginated = Checkout.query.order_by(order_by).paginate(page=page, per_page=per_page, error_out=False)

    return jsonify({
        "checkouts": [checkout.serialize() for checkout in checkouts_paginated.items],
        "total": checkouts_paginated.total,
        "page": checkouts_paginated.page,
        "pages": checkouts_paginated.pages
    })

# create a checkout that goes into effect immediately
@checkouts_bp.route("/", methods=["POST"], strict_slashes=False)
@jwt_required()
@role_required('librarian')
def create_checkout():
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

    # ensure an active checkout doesn't already exist for this user & book, ensure the book and user exists
    user = User.query.session.get(User, user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404

    book = Book.query.session.get(Book, book_id)
    if not book:
        return jsonify({"message": "Book not found"}), 404

    active_checkout = Checkout.query.filter_by(book_id=book_id, returned=False).first()
    if active_checkout:
        return jsonify({"message": "This book is already checked out"}), 400

    actively_reserved = Reservation.query.filter_by(book_id=book_id, status='active').first()
    if actively_reserved:
        if actively_reserved.user_id != user_id:
            return jsonify({"message": "This book is actively reserved by someone else"}), 400
    
        try:
            actively_reserved.status = 'fulfilled'
            actively_reserved.expires_at = None
            db.session.commit()
        except Exception as e:
            return jsonify({"message": "Something went wrong, please try again"}), 500

    # create the new checkout
    new_checkout = Checkout(
        user_id = user_id,
        book_id = book_id
    )

    try:
        db.session.add(new_checkout)
        db.session.commit()
    except Exception as e:
        return jsonify({"message": "Something went wrong, please try again"}), 500

    return jsonify({"message": f"Checkout created!"}), 201

# check a book in
@checkouts_bp.route("/<int:checkout_id>", methods=["PATCH"], strict_slashes=False)
@jwt_required()
@role_required('librarian')
def check_in_book(checkout_id):
    checkout = Checkout.query.session.get(Checkout, checkout_id)
    if not checkout:
        return jsonify({"message": "Checkout record not found"}), 404
    
    if checkout.returned == True:
        return jsonify({"message": "Book already checked in"}), 200

    # this promotes a waiting reservation to active
    book_id = checkout.book_id
    waiting_reservation = Reservation.query.filter_by(book_id=book_id, status='waiting').first()
    if waiting_reservation:
        try:
            waiting_reservation.status = 'active'
            waiting_reservation.expires_at = datetime.utcnow() + timedelta(hours=96)
            db.session.commit()
        except Exception as e:
            return jsonify({"message": "Something went wrong, please try again"}), 500

    try:
        checkout.returned = True
        db.session.commit()
    except Exception as e:
        return jsonify({"message": "Something went wrong, please try again"}), 500

    return jsonify({"message": "Book checked in"}), 201

# get your own checkouts
@checkouts_bp.route("/my", methods=["GET"], strict_slashes=False)
@jwt_required()
def get_my_checkouts():
    current_user = get_jwt_identity()
    user = User.query.session.get(User, current_user)
    if not user:
        return jsonify({"message": "User not found"}), 404

    checkouts_by_user = Checkout.query.filter_by(user_id=user.id).all()
    if not checkouts_by_user:
        return jsonify({"checkouts": []}), 200

    json_checkouts = list(map(lambda x: x.serialize(), checkouts_by_user))
    
    return jsonify({"checkouts": json_checkouts}), 200
