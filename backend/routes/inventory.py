# backend/routes/inventory.py
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.inventory import Inventory
from app import db
from utils.decorators import role_required
from datetime import datetime

inventory_bp = Blueprint('inventory', __name__)

# GET all inventory items (Storekeeper, CEO)
@inventory_bp.route('/', methods=['GET'])
@jwt_required()
@role_required(['storekeeper', 'ceo'])
def get_inventory():
    items = Inventory.query.all()
    inventory_list = [
        {
            "id": item.id,
            "name": item.name,
            "quantity": item.quantity,
            "fruit_type": item.fruit_type,
            "location": item.location,
            "expiry_date": item.expiry_date.isoformat() if item.expiry_date else None,
            "added_by": item.added_by,
            "created_at": item.created_at.isoformat()
        }
        for item in items
    ]
    return jsonify({"success": True, "data": inventory_list, "message": "Inventory items retrieved"}), 200

# POST a new inventory item (Storekeeper)
@inventory_bp.route('/', methods=['POST'])
@jwt_required()
@role_required('storekeeper')
def create_inventory_item():
    data = request.get_json()
    user_id = get_jwt_identity().get('id')
    name = data.get('name')
    quantity = data.get('quantity')
    fruit_type = data.get('fruit_type')
    location = data.get('location')
    expiry_date_str = data.get('expiry_date')

    if not all([name, quantity, fruit_type]):
        return jsonify({"success": False, "errors": ["Missing required fields"]}), 400

    try:
        expiry_date = datetime.strptime(expiry_date_str, '%Y-%m-%d').date() if expiry_date_str else None
    except ValueError:
        return jsonify({"success": False, "errors": ["Invalid date format. Use YYYY-MM-DD"]}), 400

    new_item = Inventory(
        name=name,
        quantity=quantity,
        fruit_type=fruit_type,
        location=location,
        expiry_date=expiry_date,
        added_by=user_id
    )
    db.session.add(new_item)
    db.session.commit()

    return jsonify({"success": True, "data": {"id": new_item.id}, "message": "Inventory item created"}), 201

# PUT/UPDATE an inventory item (Storekeeper)
@inventory_bp.route('/<int:item_id>', methods=['PUT'])
@jwt_required()
@role_required('storekeeper')
def update_inventory_item(item_id):
    item = Inventory.query.get(item_id)
    if not item:
        return jsonify({"success": False, "errors": ["Inventory item not found"]}), 404

    data = request.get_json()
    item.name = data.get('name', item.name)
    item.quantity = data.get('quantity', item.quantity)
    item.fruit_type = data.get('fruit_type', item.fruit_type)
    item.location = data.get('location', item.location)
    
    expiry_date_str = data.get('expiry_date')
    if expiry_date_str:
        try:
            item.expiry_date = datetime.strptime(expiry_date_str, '%Y-%m-%d').date()
        except ValueError:
            return jsonify({"success": False, "errors": ["Invalid date format. Use YYYY-MM-DD"]}), 400

    db.session.commit()
    return jsonify({"success": True, "message": "Inventory item updated successfully"}), 200

# DELETE an inventory item (Storekeeper)
@inventory_bp.route('/<int:item_id>', methods=['DELETE'])
@jwt_required()
@role_required('storekeeper')
def delete_inventory_item(item_id):
    item = Inventory.query.get(item_id)
    if not item:
        return jsonify({"success": False, "errors": ["Inventory item not found"]}), 404

    db.session.delete(item)
    db.session.commit()
    return jsonify({"success": True, "message": "Inventory item deleted successfully"}), 200

# DELETE all inventory items (Storekeeper, CEO)
@inventory_bp.route('/clear', methods=['DELETE'])
@jwt_required()
@role_required(['storekeeper', 'ceo'])
def clear_inventory():
    Inventory.query.delete()
    db.session.commit()
    return jsonify({"success": True, "message": "All inventory items cleared successfully"}), 200