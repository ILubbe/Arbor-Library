from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from models import db, SearchableMixin, User, Book, Genre, Reservation, Checkout
from config import app
from search import *
from utils.rbac_decorators import *

# define blueprint
search_bp = Blueprint('search', __name__, url_prefix='/search')

@jwt_required()
@role_required('librarian')
def privileged_search(query, page, per_page, field, model):
    # Perform the search using the search method from SearchableMixin
    if field:
        query_result, total = model.search(query, page, per_page, field)
    else:
        query_result, total = model.search(query, page, per_page)

    results = [result.serialize() for result in query_result]
    
    return jsonify({
        "total": total,
        "page": page,
        "per_page": per_page,
        "results": results
    }), 200

@search_bp.route('/', methods=["GET"], strict_slashes=False)
@jwt_required()
def search():
    model = request.args.get('model')
    query = request.args.get('query')
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('limit', 20))
    field = request.args.get('field') # optional

    if field:
        field = field.replace("-", "_") # change field from URL friendly to DB friendly

    if not model or not query:
        return jsonify({"message": "Query and Model is required in search"}), 400

    model = model.capitalize()

    searchable_models = [
        'User',
        'Book',
        'Genre',
        'Reservation',
        'Checkout'
    ]

    if model not in searchable_models:
        return jsonify({"message": f"model {model} is not valid"}), 400

    model = globals().get(model) # change model from string to class
    if not model:
        return jsonify({"message": f"model {model} is not valid"}), 400

    if model == User:
        return privileged_search(query, page, per_page, field, model)

    if field:
        query_result, total = model.search(query, page, per_page, field)
    else:
        query_result, total = model.search(query, page, per_page)

    results = [result.serialize() for result in query_result]

    return jsonify({
        "total": total,
        "page": page,
        "per_page": per_page,
        "results": results
    }), 200
