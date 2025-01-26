from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, create_access_token, create_refresh_token, get_jwt_identity
from flask_bcrypt import Bcrypt
from models import User
from config import bcrypt
from utils.general_utils import check_required_fields

# define blueprint
login_bp = Blueprint('login', __name__, url_prefix='/login')

@login_bp.route('/', methods=["POST"], strict_slashes=False)
def login():
    required_fields = [
        "email",
        "password"
    ]

    # validation for required fields
    has_all_fields, msg = check_required_fields(required_fields)
    if not has_all_fields:
        return jsonify({
            "message": f"Please fill all required fields: {', '.join(msg)}"
        }), 400

    email = request.json.get('email', None)
    password = request.json.get('password', None)

    user = User.query.filter_by(email=email).first()

    if not user or not bcrypt.check_password_hash(user.password_hash, password):
        return jsonify({"message": "Invalid credentials"}), 401

    access_token = create_access_token(identity=str(user.id))

    refresh_token = create_refresh_token(identity=str(user.id))

    return jsonify(accessToken=access_token, refreshToken=refresh_token), 200

@login_bp.route('/refresh', methods=["POST"], strict_slashes=False)
@jwt_required(refresh=True)
def refresh():
    current_user = get_jwt_identity()
    new_access_token = create_access_token(identity=current_user)

    return jsonify(accessToken=new_access_token), 200

@login_bp.route('/', methods=["GET"], strict_slashes=False)
@jwt_required()
def protected():
    current_user = get_jwt_identity()

    return jsonify(loggedInAs=current_user), 200
