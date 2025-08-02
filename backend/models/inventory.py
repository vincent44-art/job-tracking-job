from extensions import db
from datetime import datetime, date

class Inventory(db.Model):
    __tablename__ = 'inventory'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    fruit_type = db.Column(db.String(50), nullable=False)
    location = db.Column(db.String(100))
    expiry_date = db.Column(db.Date)
    added_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', backref='inventories')