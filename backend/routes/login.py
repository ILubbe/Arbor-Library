from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, create_access_token, create_refresh_token, get_jwt, get_jwt_identity
from flask_bcrypt import Bcrypt
from models import User
from config import bcrypt, r, jwt
from utils.general_utils import check_required_fields

# define blueprint
login_bp = Blueprint('login', __name__, url_prefix='/')

@login_bp.route('/login', methods=["POST"], strict_slashes=False)
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

    access_token = create_access_token(identity=str(user.id), additional_claims={"role": user.role})

    refresh_token = create_refresh_token(identity=str(user.id))

    print(f"{email} (id: {user.id}) has logged in")

    return jsonify(accessToken=access_token, refreshToken=refresh_token), 200

@login_bp.route('/login', methods=["GET"], strict_slashes=False)
@jwt_required()
def protected():
    current_user = get_jwt_identity()

    return jsonify(loggedInAs=current_user), 200

@jwt.token_in_blocklist_loader
def check_if_refresh_token_is_revoked(jwt_header, jwt_payload):
    jti = jwt_payload['jti']
    if r.get(jti):
        return True
    return False

@login_bp.route('/refresh', methods=["POST"], strict_slashes=False)
@jwt_required(refresh=True)
def refresh():
    # get refresh token's identifier
    current_user = get_jwt_identity()
    current_refresh_token_jti = get_jwt()['jti']

    # set token as revoked with ttl of 30 days in redis
    r.setex(current_refresh_token_jti, 60 * 60 * 24 * 30, "revoked")

    user = User.query.session.get(User, current_user)
    new_access_token = create_access_token(identity=current_user, additional_claims={"role": user.role})
    new_refresh_token = create_refresh_token(identity=current_user)

    return jsonify(accessToken=new_access_token, refreshToken=new_refresh_token), 201

# revokes a refresh token
@login_bp.route('/logout', methods=["POST"], strict_slashes=False)
@jwt_required(refresh=True)
def logout():
    # get refresh token's identifier
    current_user = get_jwt_identity()
    current_refresh_token_jti = get_jwt()['jti']

    # set token as revoked with ttl of 30 days in redis
    r.setex(current_refresh_token_jti, 60 * 60 * 24 * 30, "revoked")

    user = User.query.session.get(User, current_user)
    print(f"{user.email} (id: {user.id}) has logged out")

    return jsonify({"message": "Successfully logged out, please close your browser"}), 201
