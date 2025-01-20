from flask import Blueprint, request, jsonify
from models import User, db

# define blueprint
users_bp = Blueprint('users', __name__, url_prefix='/users')

# read all users
@users_bp.route("/", methods=["GET"])
def get_users():
    users = User.query.all()
    json_users = list(map(lambda x: x.user_to_json(), users))
    return jsonify({"users": json_users})
