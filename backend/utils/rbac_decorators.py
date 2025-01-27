from flask import jsonify
from flask_jwt_extended import get_jwt, get_jwt_identity, jwt_required
from functools import wraps

# Used to enforce the 'librarian' (admin) role for certain endpoints
def role_required(role):
    def decorator(fn):
        @wraps(fn)
        @jwt_required()
        def wrapper(*args, **kwargs):
            current_user = get_jwt_identity()
            current_role = get_jwt()['role']

            if current_role != role:
                return jsonify(message="Forbidden: You do not have the necessary role for this operation"), 403

            return fn(*args, **kwargs)

        return wrapper
    
    return decorator