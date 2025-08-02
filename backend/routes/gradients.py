# backend/routes/gradients.py
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.gradient import Gradient
from app import db
from utils.decorators import role_required
from datetime import datetime

gradients_bp = Blueprint('gradients', __name__)

# GET all gradients (Storekeeper, CEO)
@gradients_bp.route('/', methods=['GET'])
@jwt_required()
@role_required(['storekeeper', 'ceo'])
def get_gradients():
    gradients = Gradient.query.all()
    gradient_list = [
        {
            "id": gradient.id,
            "fruit_type": gradient.fruit_type,
            "gradient_type": gradient.gradient_type,
            "application_date": gradient.application_date.isoformat(),
            "notes": gradient.notes,
            "applied_by": gradient.applied_by,
            "created_at": gradient.created_at.isoformat()
        }
        for gradient in gradients
    ]
    return jsonify({"success": True, "data": gradient_list, "message": "Gradients retrieved"}), 200

# POST a new gradient application (Storekeeper)
@gradients_bp.route('/', methods=['POST'])
@jwt_required()
@role_required('storekeeper')
def create_gradient():
    data = request.get_json()
    user_id = get_jwt_identity().get('id')

    fruit_type = data.get('fruit_type')
    gradient_type = data.get('gradient_type')
    application_date_str = data.get('application_date')
    notes = data.get('notes')

    if not all([fruit_type, gradient_type, application_date_str]):
        return jsonify({"success": False, "errors": ["Missing required fields"]}), 400

    try:
        application_date = datetime.strptime(application_date_str, '%Y-%m-%d').date()
    except ValueError:
        return jsonify({"success": False, "errors": ["Invalid date format. Use YYYY-MM-DD"]}), 400

    new_gradient = Gradient(
        fruit_type=fruit_type,
        gradient_type=gradient_type,
        application_date=application_date,
        notes=notes,
        applied_by=user_id
    )
    db.session.add(new_gradient)
    db.session.commit()

    return jsonify({"success": True, "data": {"id": new_gradient.id}, "message": "Gradient application recorded successfully"}), 201

# DELETE a gradient application (Storekeeper, CEO)
@gradients_bp.route('/<int:gradient_id>', methods=['DELETE'])
@jwt_required()
@role_required(['storekeeper', 'ceo'])
def delete_gradient(gradient_id):
    gradient = Gradient.query.get(gradient_id)
    if not gradient:
        return jsonify({"success": False, "errors": ["Gradient not found"]}), 404

    db.session.delete(gradient)
    db.session.commit()
    return jsonify({"success": True, "message": "Gradient deleted successfully"}), 200

# DELETE all gradient applications (Storekeeper, CEO)
@gradients_bp.route('/clear', methods=['DELETE'])
@jwt_required()
@role_required(['storekeeper', 'ceo'])
def clear_gradients():
    Gradient.query.delete()
    db.session.commit()
    return jsonify({"success": True, "message": "All gradient applications cleared successfully"}), 200