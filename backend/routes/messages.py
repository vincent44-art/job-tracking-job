# backend/routes/messages.py
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.message import Message
from models.user import UserRole
from app import db
from utils.decorators import role_required
from datetime import datetime

messages_bp = Blueprint('messages', __name__)

# GET messages for the current user's role
@messages_bp.route('/', methods=['GET'])
@jwt_required()
def get_messages():
    user_info = get_jwt_identity()
    user_role = user_info['role']
    
    # Get messages addressed to the current user's role or all roles
    messages = Message.query.filter(
        (Message.recipient_role == UserRole[user_role.upper()]) | (Message.recipient_role == None)
    ).order_by(Message.created_at.desc()).all()

    message_list = [
        {
            "id": msg.id,
            "sender_id": msg.sender_id,
            "recipient_role": msg.recipient_role.value if msg.recipient_role else None,
            "message": msg.message,
            "is_read": msg.is_read,
            "created_at": msg.created_at.isoformat()
        }
        for msg in messages
    ]
    return jsonify({"success": True, "data": message_list, "message": "Messages retrieved"}), 200

# POST a new message (CEO only)
@messages_bp.route('/', methods=['POST'])
@jwt_required()
@role_required('ceo')
def create_message():
    data = request.get_json()
    sender_id = get_jwt_identity().get('id')

    recipient_role_str = data.get('recipient_role')
    message_text = data.get('message')

    if not message_text:
        return jsonify({"success": False, "errors": ["Message text is required"]}), 400

    recipient_role = None
    if recipient_role_str:
        try:
            recipient_role = UserRole[recipient_role_str.upper()]
        except KeyError:
            return jsonify({"success": False, "errors": ["Invalid recipient role"]}), 400

    new_message = Message(
        sender_id=sender_id,
        recipient_role=recipient_role,
        message=message_text
    )
    db.session.add(new_message)
    db.session.commit()

    return jsonify({"success": True, "data": {"id": new_message.id}, "message": "Message sent successfully"}), 201

# Mark a message as read
@messages_bp.route('/<int:message_id>/read', methods=['PUT'])
@jwt_required()
def mark_message_as_read(message_id):
    message = Message.query.get(message_id)
    if not message:
        return jsonify({"success": False, "errors": ["Message not found"]}), 404

    message.is_read = True
    db.session.commit()
    return jsonify({"success": True, "message": "Message marked as read"}), 200

# DELETE all messages (CEO only)
@messages_bp.route('/clear', methods=['DELETE'])
@jwt_required()
@role_required('ceo')
def clear_messages():
    Message.query.delete()
    db.session.commit()
    return jsonify({"success": True, "message": "All messages cleared successfully"}), 200