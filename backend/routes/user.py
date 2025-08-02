# backend/routes/user.py
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from models.user import User, UserRole
from app import db
from utils.decorators import role_required
from werkzeug.security import generate_password_hash

user_bp = Blueprint('user', __name__)

# GET all users (CEO only)
@user_bp.route('/', methods=['GET'])
@jwt_required()
@role_required('ceo')
def get_users():
    users = User.query.all()
    user_list = [
        {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "role": user.role.value,
            "salary": user.salary,
            "is_paid": user.is_paid,
            "is_active": user.is_active,
            "created_at": user.created_at.isoformat()
        }
        for user in users
    ]
    return jsonify({"success": True, "data": user_list, "message": "Users retrieved"}), 200

# POST a new user (CEO only)
@user_bp.route('/', methods=['POST'])
@jwt_required()
@role_required('ceo')
def create_user():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    name = data.get('name')
    role_str = data.get('role')
    salary = data.get('salary', 0.0)

    if not all([email, password, name, role_str]):
        return jsonify({"success": False, "errors": ["Missing required fields"]}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({"success": False, "errors": ["User with this email already exists"]}), 409

    try:
        user_role = UserRole[role_str.upper()]
    except KeyError:
        return jsonify({"success": False, "errors": ["Invalid role specified"]}), 400

    new_user = User(
        name=name,
        email=email,
        password_hash=generate_password_hash(password),
        role=user_role,
        salary=salary
    )
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"success": True, "data": {"id": new_user.id}, "message": "User created successfully"}), 201

# PUT/UPDATE a user (CEO only)
@user_bp.route('/<int:user_id>', methods=['PUT'])
@jwt_required()
@role_required('ceo')
def update_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"success": False, "errors": ["User not found"]}), 404

    data = request.get_json()
    user.name = data.get('name', user.name)
    user.email = data.get('email', user.email)
    user.salary = data.get('salary', user.salary)
    
    # Allow changing role
    role_str = data.get('role')
    if role_str:
        try:
            user.role = UserRole[role_str.upper()]
        except KeyError:
            return jsonify({"success": False, "errors": ["Invalid role specified"]}), 400

    # Allow changing password
    new_password = data.get('password')
    if new_password:
        user.password_hash = generate_password_hash(new_password)

    db.session.commit()
    return jsonify({"success": True, "message": "User updated successfully"}), 200

# DELETE a user (CEO only)
@user_bp.route('/<int:user_id>', methods=['DELETE'])
@jwt_required()
@role_required('ceo')
def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"success": False, "errors": ["User not found"]}), 404

    db.session.delete(user)
    db.session.commit()
    return jsonify({"success": True, "message": "User deleted successfully"}), 200

# PUT to update salary (CEO only)
@user_bp.route('/<int:user_id>/salary', methods=['PUT'])
@jwt_required()
@role_required('ceo')
def update_salary(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"success": False, "errors": ["User not found"]}), 404

    data = request.get_json()
    new_salary = data.get('salary')
    if not isinstance(new_salary, (int, float)):
        return jsonify({"success": False, "errors": ["Salary must be a number"]}), 400

    user.salary = new_salary
    db.session.commit()
    return jsonify({"success": True, "message": "User salary updated successfully"}), 200

# PUT to pay salary (CEO only)
@user_bp.route('/<int:user_id>/pay-salary', methods=['PUT'])
@jwt_required()
@role_required('ceo')
def pay_salary(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"success": False, "errors": ["User not found"]}), 404

    user.is_paid = True
    db.session.commit()
    return jsonify({"success": True, "message": f"Salary for {user.name} marked as paid"}), 200