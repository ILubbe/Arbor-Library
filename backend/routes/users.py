import re
from flask import Blueprint, request, jsonify
from models import User, db
from utils.password_utils import complexity_check, hash_salt_password

# define blueprint
users_bp = Blueprint('users', __name__, url_prefix='/users')

# read all users
@users_bp.route("/", methods=["GET"], strict_slashes=False)
def get_users():
    users = User.query.all()
    json_users = list(map(lambda x: x.user_to_json(), users))
    return jsonify({"users": json_users})

# create a user
@users_bp.route("/", methods=["POST"], strict_slashes=False)
def create_user():
    required_fields = [
        "role",
        "username",
        "password",
        "passwordConfirmation",
        "firstName",
        "lastName"
    ]

    # check if any required field is missing, convert from camel to spaces for user readability
    missing_fields = [re.sub( '(?<!^)(?=[A-Z])', ' ', field ).lower() for field in required_fields if not request.json.get(field)]

    if missing_fields:
        return (
            jsonify({"message": f"Please fill all required fields: {', '.join(missing_fields)}"}),
            400,
        )

    role = request.json.get("role")
    username = request.json.get("username")
    password = request.json.get("password") # plain text
    password_confirmation = request.json.get("passwordConfirmation")  # plain text password confirmation
    first_name = request.json.get("firstName")
    last_name = request.json.get("lastName")

    existing_username = User.query.filter_by(username = username).first()
    if existing_username:
        return jsonify({"message": "That username is unavailable"}), 400

    if password != password_confirmation:
        return jsonify({"message": "Passwords do not match"})

    password_min_length = 12
    if not complexity_check(password, password_min_length):
        message = (
            f"Password must meet that following complexity requirements:\n"
            "  - At least {password_min_length} characters long\n"  
            "  - Include at least one uppercase letter\n"
            "  - Include at least one lowercase letter\n"
            "  - Include at least one digit\n"
            "  - Include at least one special character."
        )
        
        return jsonify({
            "message": message
        }), 400

    new_user = User(
        role = role,
        username = username,
        password_hash = hash_salt_password(password), # store salted hash as a string
        first_name = first_name,
        last_name = last_name
    )

    try:
        db.session.add(new_user)
        db.session.commit()
    except Exception as e:
        return jsonify({"message": str(e)}), 400

    return jsonify({"message": f"User {username} created!"}), 201
    
