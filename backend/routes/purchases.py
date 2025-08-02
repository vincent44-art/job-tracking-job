# backend/routes/purchases.py
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from utils.decorators import role_required
# from models.purchases import Purchase
# from app import db

purchases_bp = Blueprint('purchases', __name__)

@purchases_bp.route('/', methods=['GET'])
@jwt_required()
@role_required('purchaser')
def get_purchases():
    # Logic to get purchases for the current purchaser
    return jsonify({"success": True, "data": [], "message": "Purchases retrieved"}), 200

# Add other CRUD routes here...