from extensions import db
from datetime import datetime, date
import enum

class MovementType(enum.Enum):
    IN = "in"
    OUT = "out"

class StockMovement(db.Model):
    __tablename__ = 'stock_movements'

    id = db.Column(db.Integer, primary_key=True)
    fruit_type = db.Column(db.String(50), nullable=False)
    movement_type = db.Column(db.Enum(MovementType), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    date = db.Column(db.Date, default=date.today)
    notes = db.Column(db.String(255))
    added_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', backref='stock_movements')