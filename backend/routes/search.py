from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from models import db, SearchableMixin, User, Book, Genre, Reservation, Checkout
from config import app
from search import *
from utils.rbac_decorators import *

# define blueprint
search_bp = Blueprint('search', __name__, url_prefix='/search')

@jwt_required()
def check_index_exists(model):
    index_name = model.__tablename__.lower()
    if not app.es.indices.exists(index=index_name):
        return False
    return True

@jwt_required()
def is_valid_field(model, field):
    # check if the field exists in the model's columns
    if hasattr(model, '__table__') and field in model.__table__.columns:
        return True
    # check if the field exists as a relationship
    if hasattr(model, '__mapper__') and field in model.__mapper__.relationships:
        return True
    return False

@jwt_required()
@role_required('librarian')
# only for librarians to search users
def privileged_search(query, page, per_page, field, model):
    # if the index doesn't exist, just give a response like it does.
    # This means that the db table is empty for that model, so elasticsearch never made an index.
    if not check_index_exists(model):
        results = []
        total = 0
        return jsonify({
            "total": total,
            "page": page,
            "per_page": per_page,
            "results": results
        }), 200

    if field:
        if not is_valid_field(model, field):
            return({"message": f"field {field} is not valid for this model"}), 400
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

    model = model.lower().capitalize()

    searchable_models = [
        'User',
        'Book',
        'Reservation',
        'Checkout'
    ]

    if model not in searchable_models:
        return jsonify({"message": f"model {model} is not valid"}), 400

    model = globals().get(model) # change model from string to class

    if model == User or model == Reservation or model == Checkout:
        return privileged_search(query, page, per_page, field, model)

    # if the index doesn't exist, just give a response like it does.
    # This means that the db table is empty for that model, so elasticsearch never made an index.
    if not check_index_exists(model):
        results = []
        total = 0
        return jsonify({
            "total": total,
            "page": page,
            "per_page": per_page,
            "results": results
        }), 200

    if field:
        if not is_valid_field(model, field.lower()):
            return({"message": f"field {field} is not valid for this model"}), 400
        # use a different search method if field is genre
        if field.lower() == 'genre':
            query_result, total = model.search_books_by_genre(query, page, per_page)
        else:
            query_result, total = model.search(query, page, per_page, field)
    else:
        query_result, total = model.search(query, page, per_page)

    results = []
    for item in query_result:
        item_data = item.serialize()
        if hasattr(item, 'genres'):
            item_data['genres'] = [genre.genre for genre in item.genres]
        
        results.append(item_data)

    return jsonify({
        "total": total,
        "page": page,
        "per_page": per_page,
        "results": results
    }), 200
