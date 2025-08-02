from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.user import User
from models.sales import Sale
from models.purchases import Purchase
from models.inventory import Inventory
from extensions import db
from sqlalchemy import func
from datetime import date, timedelta

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/overview', methods=['GET'])
@jwt_required()
def get_dashboard_overview():
    current_user_id = get_jwt_identity()['id']
    user = User.query.get(current_user_id)
    
    data = {
        'username': user.name,
        'role': user.role.value,
    }

    if user.role.value == 'ceo':
        total_revenue = db.session.query(func.sum(Sale.revenue)).scalar() or 0
        total_expenses = db.session.query(func.sum(Purchase.cost)).scalar() or 0
        total_profit = total_revenue - total_expenses
        total_users = User.query.count()
        
        data['total_revenue'] = float(total_revenue)
        data['total_expenses'] = float(total_expenses)
        data['total_profit'] = float(total_profit)
        data['total_users'] = total_users
        
        return jsonify({'message': 'CEO dashboard data fetched successfully', 'data': data}), 200
    
    elif user.role.value == 'storekeeper':
        # Get total stock level from all inventory
        total_stock = db.session.query(func.sum(Inventory.stock_level)).scalar() or 0
        # Get pending orders (for now, we'll just return a dummy value)
        pending_orders = 15
        
        data['stock_level'] = total_stock
        data['pending_orders'] = pending_orders
        
        return jsonify({'message': 'Storekeeper dashboard data fetched successfully', 'data': data}), 200
        
    elif user.role.value == 'seller':
        # Calculate sales for today
        today = date.today()
        sales_today = db.session.query(func.sum(Sale.revenue)).filter(func.date(Sale.created_at) == today).scalar() or 0
        
        # Get customers served (dummy data for now, as we don't have a specific customer model yet)
        customers_served = 15
        
        data['sales_today'] = float(sales_today)
        data['customers_served'] = customers_served
        
        return jsonify({'message': 'Seller dashboard data fetched successfully', 'data': data}), 200
    
    elif user.role.value == 'purchaser':
        # Get total pending purchases (dummy data for now)
        pending_purchases = 5
        
        data['pending_purchases'] = pending_purchases
        data['suppliers'] = ['Supplier A', 'Supplier B']
        
        return jsonify({'message': 'Purchaser dashboard data fetched successfully', 'data': data}), 200

    elif user.role.value == 'driver':
        # Get pending and completed deliveries (dummy data for now)
        pending_deliveries = 3
        completed_deliveries = 7
        
        data['pending_deliveries'] = pending_deliveries
        data['completed_deliveries'] = completed_deliveries
        data['delivery_schedule'] = ['Store A', 'Store B']
        
        return jsonify({'message': 'Driver dashboard data fetched successfully', 'data': data}), 200

    return jsonify({'message': 'User role not supported'}), 403