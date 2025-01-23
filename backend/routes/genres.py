from flask import Blueprint, request, jsonify
from models import Genre, db
from utils.general_utils import *

# define blueprint
genres_bp = Blueprint('genres', __name__, url_prefix='/genres')

# read all genres
@genres_bp.route("/", methods=["GET"], strict_slashes=False)
def get_genres():
    genres = Genre.query.all()
    json_genres = list(map(lambda x: x.genre_to_json(), genres))
    return jsonify({"genres": json_genres})

# get one genre
@genres_bp.route("/<int:genre_id>", methods=["GET"])
def get_one_genre(genre_id):
    genre = Genre.query.get(genre_id)

    if genre is None:
        return jsonify({"message": "Genre not found"}), 404
    
    return jsonify({"genre": genre.genre_to_json()})

# create a genre
@genres_bp.route("/", methods=["POST"], strict_slashes=False)
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
        return jsonify({"message": f"Something went wrong, please try again {str, e}"}), 400

    return jsonify({"message": f"Genre {genre} added!"}), 201