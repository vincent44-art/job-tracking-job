# backend/routes/stock.py
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.stock_movement import StockMovement
from app import db
from utils.decorators import role_required
from datetime import datetime

stock_bp = Blueprint('stock', __name__)

# GET all stock movements (Storekeeper, CEO)
@stock_bp.route('/movements', methods=['GET'])
@jwt_required()
@role_required(['storekeeper', 'ceo'])
def get_stock_movements():
    movements = StockMovement.query.all()
    movement_list = [
        {
            "id": movement.id,
            "fruit_type": movement.fruit_type,
            "movement_type": movement.movement_type,
            "quantity": movement.quantity,
            "date": movement.date.isoformat(),
            "notes": movement.notes,
            "added_by": movement.added_by,
            "created_at": movement.created_at.isoformat()
        }
        for movement in movements
    ]
    return jsonify({"success": True, "data": movement_list, "message": "Stock movements retrieved"}), 200

# POST a new stock movement (Storekeeper)
@stock_bp.route('/movements', methods=['POST'])
@jwt_required()
@role_required('storekeeper')
def create_stock_movement():
    data = request.get_json()
    user_id = get_jwt_identity().get('id')
    
    fruit_type = data.get('fruit_type')
    movement_type = data.get('movement_type')
    quantity = data.get('quantity')
    date_str = data.get('date')
    notes = data.get('notes')

    if not all([fruit_type, movement_type, quantity, date_str]):
        return jsonify({"success": False, "errors": ["Missing required fields"]}), 400

    if movement_type not in ['in', 'out']:
        return jsonify({"success": False, "errors": ["Movement type must be 'in' or 'out'"]}), 400

    try:
        date = datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
        return jsonify({"success": False, "errors": ["Invalid date format. Use YYYY-MM-DD"]}), 400

    new_movement = StockMovement(
        fruit_type=fruit_type,
        movement_type=movement_type,
        quantity=quantity,
        date=date,
        notes=notes,
        added_by=user_id
    )
    db.session.add(new_movement)
    db.session.commit()
    
    return jsonify({"success": True, "data": {"id": new_movement.id}, "message": "Stock movement recorded successfully"}), 201

# DELETE a stock movement (Storekeeper, CEO)
@stock_bp.route('/movements/<int:movement_id>', methods=['DELETE'])
@jwt_required()
@role_required(['storekeeper', 'ceo'])
def delete_stock_movement(movement_id):
    movement = StockMovement.query.get(movement_id)
    if not movement:
        return jsonify({"success": False, "errors": ["Stock movement not found"]}), 404

    db.session.delete(movement)
    db.session.commit()
    return jsonify({"success": True, "message": "Stock movement deleted successfully"}), 200

# DELETE all stock movements (Storekeeper, CEO)
@stock_bp.route('/movements/clear', methods=['DELETE'])
@jwt_required()
@role_required(['storekeeper', 'ceo'])
def clear_stock_movements():
    StockMovement.query.delete()
    db.session.commit()
    return jsonify({"success": True, "message": "All stock movements cleared successfully"}), 200