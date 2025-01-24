from flask import Blueprint, request, jsonify
from sqlalchemy import func
from models import Checkout, User, Book, Reservation, db
from utils.general_utils import *

# define blueprint
checkouts_bp = Blueprint('checkouts', __name__, url_prefix='/checkouts')

# get all checkouts
@checkouts_bp.route("/", methods=["GET"], strict_slashes=False)
def get_checkouts():
    checkouts = Checkout.query.all()
    json_checkouts = list(map(lambda x: x.checkout_to_json(), checkouts))
    return jsonify({"checkouts": json_checkouts})

# get a checkout by id
@checkouts_bp.route("/<int:checkout_id>", methods=["GET"], strict_slashes=False)
def get_checkout_by_id(checkout_id):
    checkout = Checkout.query.get(checkout_id)

    if checkout is None:
        return jsonify({"message": "Checkout not found"}), 404
    
    return jsonify({"checkout": checkout.checkout_to_json()})

# get checkout(s) by user
@checkouts_bp.route("/by-user/<int:user_id>", methods=["GET"], strict_slashes=False)
def get_checkouts_by_user(user_id):
    # ensure user exists
    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404

    checkouts_by_user = Checkout.query.filter_by(user_id=user_id).all()
    if not checkouts_by_user:
        return jsonify({"message": "No checkouts associated with this user"}), 404

    checkout_ids = [checkout.id for checkout in checkouts_by_user]
    
    return jsonify({"checkoutsIdByUser": checkout_ids}), 200

# get all checkout(s) made for one book
@checkouts_bp.route("/by-book/<int:book_id>", methods=["GET"], strict_slashes=False)
def get_checkouts_by_book(book_id):
    # ensure book exists
    book = Book.query.get(book_id)
    if not book:
        return jsonify({"message": "Book not found"}), 404

    checkouts_by_book = Checkout.query.filter_by(book_id=book_id).all()
    if not checkouts_by_book:
        return jsonify({"message": "No checkouts associated with this book"}), 404

    checkout_ids = [checkout.id for checkout in checkouts_by_book]
    
    return jsonify({"checkoutsIdByBook": checkout_ids}), 200

# get active checkout(s) by user (not yet returned)
@checkouts_bp.route("/by-user/active/<int:user_id>", methods=["GET"], strict_slashes=False)
def get_active_checkouts_by_user(user_id):
    # ensure user exists
    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404

    active_checkouts_by_user = Checkout.query.filter_by(user_id=user_id, returned=False)
    if not active_checkouts_by_user:
        return jsonify({"message": "No active checkouts associated with this user"}), 404

    active_checkouts_by_user_ids = [checkout.id for checkout in active_checkouts_by_user]
    
    return jsonify({"activeCheckoutsIdByUser": active_checkouts_by_user_ids}), 200

# get active checkout(s) by book (not yet returned)
@checkouts_bp.route("/by-book/active/<int:book_id>", methods=["GET"], strict_slashes=False)
def get_active_checkouts_by_book(book_id):
    # ensure book exists
    book = Book.query.get(book_id)
    if not book:
        return jsonify({"message": "Book not found"}), 404

    active_checkouts_by_book = Checkout.query.filter_by(book_id=book_id, returned=False)
    if not active_checkouts_by_book:
        return jsonify({"message": "No active checkouts associated with this book"}), 404

    active_checkouts_by_book_ids = [checkout.id for checkout in active_checkouts_by_book]
    
    return jsonify({"activeCheckoutsIdByBook": active_checkouts_by_book_ids}), 200

# get all checkout(s) that one user has made for one book
@checkouts_bp.route("/<int:user_id>/<int:book_id>", methods=["GET"], strict_slashes=False)
def get_checkouts_by_book_and_user(user_id, book_id):
    #ensure user and book exist
    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": f"User not found"}), 404

    book = Book.query.get(book_id)
    if not book:
        return jsonify({"message": f"Book not found"}), 404

    checkouts_by_book_and_user = Checkout.query.filter_by(user_id=user_id, book_id=book_id)

    checkout_ids = [checkout.id for checkout in checkouts_by_book_and_user]

    return jsonify({"checkoutsIdByUserAndBook": checkout_ids}), 200

# create a checkout that goes into effect immediately
@checkouts_bp.route("/", methods=["POST"], strict_slashes=False)
def create_immediate_checkout():
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
    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": f"User not found"}), 404

    book = Book.query.get(book_id)
    if not book:
        return jsonify({"message": f"Book not found"}), 404

    active_checkout = Checkout.query.filter_by(book_id=book_id, returned=False).first()
    if active_checkout:
        return jsonify({"message": "This book is already checked out"}), 400

    actively_reserved = Reservation.query.filter_by(book_id=book_id, status='active').first()
    if actively_reserved:
        if actively_reserved.user_id != user_id:
            return jsonify({"message": "This book is actively reserved by someone else"}), 400
    
        try:
            actively_reserved.status = 'fulfilled'
            db.session.commit()
        except Exception as e:
            return jsonify({"message": f"Something went wrong, please try again"}), 400
        
        return jsonify({"message": f"Checkout created! Active reservation status changed to 'fulfilled'"}), 201
    

    # create the new checkout
    new_checkout = Checkout(
        user_id = user_id,
        book_id = book_id
    )

    try:
        db.session.add(new_checkout)
        db.session.commit()
    except Exception as e:
        return jsonify({"message": f"Something went wrong, please try again"}), 400

    return jsonify({"message": f"Checkout created!"}), 201