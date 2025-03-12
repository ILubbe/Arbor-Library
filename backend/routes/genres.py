from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from models import Genre, db
from sqlalchemy import asc, desc
from utils.general_utils import *
from utils.rbac_decorators import *

# define blueprint
genres_bp = Blueprint('genres', __name__, url_prefix='/api/genres')

# read all genres
@genres_bp.route("/", methods=["GET"], strict_slashes=False)
@jwt_required()
@role_required('librarian')
def get_genres():
    # sort & paginate 
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per-page", 50, type=int)  # default 50
    col = request.args.get("col", "id").replace("-", "_").lower()
    order = request.args.get("order", "asc")

    if not hasattr(Genre, col):
        return jsonify({"message": f"invalid column to sort by: {col}"}), 400

    sorted_column = getattr(Genre, col)
    order_by = desc(sorted_column) if order.lower() == "desc" else asc(sorted_column)

    genres_paginated = Genre.query.order_by(order_by).paginate(page=page, per_page=per_page, error_out=False)

    return jsonify({
        "genres": [genre.serialize() for genre in genres_paginated.items],
        "total": genres_paginated.total,
        "page": genres_paginated.page,
        "pages": genres_paginated.pages
    })

# create a genre
@genres_bp.route("/", methods=["POST"], strict_slashes=False)
@jwt_required()
@role_required('librarian')
def create_genre():
    required_fields = [
        "genre"
    ]

    # validation for required fields
    has_all_fields, msg = check_required_fields(required_fields)
    if not has_all_fields:
        return jsonify({
            "message": f"Please fill all required fields: {', '.join(msg)}"
        }), 400

    # convert json keys to valid db columns
    genre = request.json.get("genre")

    # does it already exist?
    existing_genre = Genre.query.filter_by(genre = genre).first()
    if existing_genre:
        return jsonify({"message": "That genre is already present"}), 400

    new_genre = Genre(
        genre = genre
    )

    # length validation
    length_ok, field = field_length_ok(Genre, new_genre)
    if not length_ok:
        field = field.replace("_", " ").title()
        return jsonify({
            "message": f"The following field is too long: {field}"
        }), 400

    try:
        db.session.add(new_genre)
        db.session.commit()
    except Exception as e:
        return jsonify({"message": "Something went wrong, please try again"}), 500

    return jsonify({"message": f"Genre {genre} added!"}), 201
