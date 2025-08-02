# backend/utils/decorators.py
from functools import wraps
from flask import jsonify
from flask_jwt_extended import get_jwt_identity

def role_required(roles):
    if not isinstance(roles, list):
        roles = [roles]
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            current_user_role = get_jwt_identity().get('role')
            if current_user_role not in roles:
                return jsonify({"success": False, "errors": [f"Access denied: Requires one of {', '.join(roles)} roles"]}), 403
            return fn(*args, **kwargs)
        return wrapper
    return decorator