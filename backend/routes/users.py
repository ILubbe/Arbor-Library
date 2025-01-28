from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import User, db
from utils.general_utils import *
from utils.password_utils import *
from utils.rbac_decorators import *


# define blueprint
users_bp = Blueprint('users', __name__, url_prefix='/users')

# get all users
@users_bp.route("/", methods=["GET"], strict_slashes=False)
@jwt_required()
@role_required('librarian')
def get_users():
    users = User.query.all()
    json_users = list(map(lambda x: x.user_to_json(), users))
    return jsonify({"users": json_users})

# get user by id
@users_bp.route("/<int:user_id>", methods=["GET"], strict_slashes=False)
@jwt_required()
@role_required('librarian')
def get_user_by_id(user_id):
    user = User.query.get(user_id)

    if not user:
        return jsonify({"message": "User not found"}), 404
    
    return jsonify({"user": user.user_to_json()}), 200

# get only your own user info
@users_bp.route("/profile", methods=["GET"], strict_slashes=False)
@jwt_required()
def get_profile():
    current_user = get_jwt_identity()
    user = User.query.filter_by(id=current_user).first()
    if not user:
        return jsonify({"message": "User not found"}), 404

    return jsonify({"user": user.user_to_json()}), 200


# create a user UNPROTECTED
@users_bp.route("/", methods=["POST"], strict_slashes=False)
def create_user():
    required_fields = [
        "email",
        "password",
        "passwordConfirmation",
        "firstName",
        "lastName"
    ]

    # validation for required fields
    has_all_fields, msg = check_required_fields(required_fields)
    if not has_all_fields:
        return jsonify({
            "message": f"Please fill all required fields: {', '.join(msg)}"
        }), 400

    # convert json keys to valid db columns
    role = "patron"
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
        return jsonify({"message": "Passwords do not match"}), 400

    password_min_length = 12
    is_valid, message = complexity_check(password, password_min_length)
    if not is_valid:
        return jsonify({
            "message": message
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
        return jsonify({"message": "Something went wrong, please try again"}), 500

    return jsonify({"message": f"User {email} created!"}), 201
    
# delete a user by id
@users_bp.route("/<int:user_id>", methods=["DELETE"], strict_slashes=False)
@jwt_required()
@role_required('librarian')
def delete_user(user_id):
    user = User.query.get(user_id)

    if not user:
        return jsonify({"message": "User not found"}), 404
    try:
        db.session.delete(user)
        db.session.commit()
    except Exception as e:
        return jsonify({"message": "Something went wrong, please try again"}), 500

    return jsonify({"message": "User deleted successfully"}), 200

# delete yourself
@users_bp.route("/profile", methods=["DELETE"], strict_slashes=False)
@jwt_required()
def delete_profile():
    current_user = get_jwt_identity()
    user = User.query.filter_by(id=current_user).first()
    if not user:
        return jsonify({"message": "User not found"}), 404
    try:
        db.session.delete(user)
        db.session.commit()
    except Exception as e:
        return jsonify({"message": "Something went wrong, please try again"}), 500

    return jsonify({"message": "User deleted successfully"}), 200

# update a user's role, change from patron to librarian or librarian to patron (toggle)
@users_bp.route("/<int:user_id>", methods=["PATCH"], strict_slashes=False)
@jwt_required()
@role_required('librarian')
def change_user_role(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404

    old_role = user.role
    new_role = 'librarian' if user.role == 'patron' else 'patron' if user.role == 'librarian' else None

    if new_role is None:
        return jsonify({"message": "Something went wrong, please try again"}), 500

    try:
        user.role = new_role
        db.session.commit()
    except Exception as e:
        return jsonify({"message": "Something went wrong, please try again"}), 500

    return jsonify({"message": f"User's role updated from {old_role} to {new_role}"}), 201

# update a user's info - password, firstname, and lastname only
@users_bp.route("/<int:user_id>", methods=["PUT"], strict_slashes=False)
@jwt_required()
@role_required('librarian')
def change_user_info(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404

    required_fields = [
        "password",
        "passwordConfirmation",
        "firstName",
        "lastName"
    ]

    # validation for required fields
    has_all_fields, msg = check_required_fields(required_fields)
    if not has_all_fields:
        return jsonify({
            "message": f"Please fill all required fields: {', '.join(msg)}"
        }), 400

    # convert json keys to valid db columns
    password = request.json.get("password") # plain text
    password_confirmation = request.json.get("passwordConfirmation")  # plain text password confirmation
    first_name = request.json.get("firstName")
    last_name = request.json.get("lastName")

    if password != password_confirmation:
        return jsonify({"message": "Passwords do not match"})

    password_min_length = 12
    is_valid, message = complexity_check(password, password_min_length)
    if not is_valid:
        return jsonify({
            "message": message
        }), 400

    updated_user = User(
        role = user.role, # not updating this
        email = user.email, # not updating this
        password_hash = hash_salt_password(password), # store salted hash as a string
        first_name = first_name,
        last_name = last_name
    )

    # validate length
    length_ok, field = field_length_ok(User, updated_user)
    if not length_ok:
        field = field.replace("_", " ").title()
        return jsonify({
            "message": f"The following field is too long: {field}"
        }), 400

    # only updating the password and name here
    try:
        user.role = updated_user.role # not updating this
        user.email = updated_user.email # not updating this
        user.password_hash = updated_user.password_hash
        user.first_name = updated_user.first_name
        user.last_name = updated_user.last_name
        db.session.commit()
    except Exception as e:

        return jsonify({"message": "Something went wrong, please try again"}), 500

    return jsonify({"message": "User udpated"}), 201

# update your own info - password, firstname, and lastname only
@users_bp.route("/profile", methods=["PUT"], strict_slashes=False)
@jwt_required()
def change_profile_info():
    current_user = get_jwt_identity()
    user = User.query.filter_by(id=current_user).first()
    if not user:
        return jsonify({"message": "User not found"}), 404

    required_fields = [
        "password",
        "passwordConfirmation",
        "firstName",
        "lastName"
    ]

    # validation for required fields
    has_all_fields, msg = check_required_fields(required_fields)
    if not has_all_fields:
        return jsonify({
            "message": f"Please fill all required fields: {', '.join(msg)}"
        }), 400

    # convert json keys to valid db columns
    password = request.json.get("password") # plain text
    password_confirmation = request.json.get("passwordConfirmation")  # plain text password confirmation
    first_name = request.json.get("firstName")
    last_name = request.json.get("lastName")

    if password != password_confirmation:
        return jsonify({"message": "Passwords do not match"})

    password_min_length = 12
    is_valid, message = complexity_check(password, password_min_length)
    if not is_valid:
        return jsonify({
            "message": message
        }), 400

    updated_user = User(
        role = user.role, # not updating this
        email = user.email, # not updating this
        password_hash = hash_salt_password(password), # store salted hash as a string
        first_name = first_name,
        last_name = last_name
    )

    # validate length
    length_ok, field = field_length_ok(User, updated_user)
    if not length_ok:
        field = field.replace("_", " ").title()
        return jsonify({
            "message": f"The following field is too long: {field}"
        }), 400

    # only updating the password and name here
    try:
        user.role = updated_user.role # not updating this
        user.email = updated_user.email # not updating this
        user.password_hash = updated_user.password_hash
        user.first_name = updated_user.first_name
        user.last_name = updated_user.last_name
        db.session.commit()
    except Exception as e:

        return jsonify({"message": "Something went wrong, please try again"}), 500

    return jsonify({"message": "Your info has been udpated"}), 201

