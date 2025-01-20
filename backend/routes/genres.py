from flask import Blueprint, request, jsonify
from backend.models import Genre, db

# define blueprint
genres_bp = Blueprint('genres', __name__, url_prefix='/genres')

# read all genres
@genres_bp.route("/", methods=["GET"], strict_slashes=False)
def get_genres():
    genres = Genre.query.all()
    json_genres = list(map(lambda x: x.genre_to_json(), genres))
    return jsonify({"genres": json_genres})