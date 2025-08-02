from flask import Blueprint, request, jsonify
from extensions import db
from models.user import User
from flask_jwt_extended import create_access_token
from datetime import timedelta

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST', 'OPTIONS'])
def login():
    # Handle the OPTIONS preflight request first, before any other logic
    if request.method == 'OPTIONS':
        return '', 204 # 204 is a "No Content" status, which is a valid OK response

    # Now handle the POST request
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()

    if user and user.check_password(password):
        # Successful login, create a token with user info
        expires = timedelta(hours=24)
        access_token = create_access_token(identity={'id': user.id, 'role': user.role.value}, expires_delta=expires)
        return jsonify(access_token=access_token), 200
    else:
        return jsonify({"msg": "Invalid email or password"}), 401