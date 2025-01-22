import re
from flask import Blueprint, request, jsonify
from models import User, db
from utils.general_utils import *
from utils.create_user_utils import *
from utils.password_utils import *


# define blueprint
users_bp = Blueprint('users', __name__, url_prefix='/users')

# get all users
@users_bp.route("/", methods=["GET"], strict_slashes=False)
def get_users():
    users = User.query.all()
    json_users = list(map(lambda x: x.user_to_json(), users))
    return jsonify({"users": json_users})

# get one user
#@users_bp.route(/)

# create a user
@users_bp.route("/", methods=["POST"], strict_slashes=False)
def create_user():
    required_fields = [
        "role",
        "email",
        "password",
        "passwordConfirmation",
        "firstName",
        "lastName"
    ]

    # validations
    has_all_fields, msg = check_required_fields(required_fields)
    if not has_all_fields:
        return jsonify({
            "message": f"Please fill all required fields: {', '.join(msg)}"
        }), 400

    # convert json keys to valid db columns
    role = request.json.get("role").lower()
    email = request.json.get("email").lower()
    password = request.json.get("password") # plain text
    password_confirmation = request.json.get("passwordConfirmation")  # plain text password confirmation
    first_name = request.json.get("firstName")
    last_name = request.json.get("lastName")

    # more validations
    existing_email = User.query.filter_by(email = email).first()
    if existing_email:
        return jsonify({"message": "That email is unavailable"}), 400

    if password != password_confirmation:
        return jsonify({"message": "Passwords do not match"})

    password_min_length = 12
    is_valid, message = complexity_check(password, password_min_length)
    if not is_valid:
        return jsonify({
            "message": message
        }), 400

    valid_roles = ["patron", "librarian"]
    if not is_role_valid(role, valid_roles):
        return jsonify({
            "message": f"Invalid role. A role can be one of the following: {', '.join(valid_roles)}"
        }), 400

    # create user
    new_user = User(
        role = role,
        email = email,
        password_hash = hash_salt_password(password), # store salted hash as a string
        first_name = first_name,
        last_name = last_name
    )

    # validate length
    length_ok, field = field_length_ok(User, new_user)
    if not length_ok:
        field = field.replace("_", " ").title()
        return jsonify({
            "message": f"The following field is too long: {field}"
        }), 400

    try:
        db.session.add(new_user)
        db.session.commit()
    except Exception as e:
        return jsonify({"message": "Something went wrong, please try again"}), 400

    return jsonify({"message": f"User {email} created!"}), 201
    
