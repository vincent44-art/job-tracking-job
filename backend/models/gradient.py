from extensions import db
from datetime import datetime, date

class Gradient(db.Model):
    __tablename__ = 'gradients'

    id = db.Column(db.Integer, primary_key=True)
    fruit_type = db.Column(db.String(50), nullable=False)
    gradient_type = db.Column(db.String(100), nullable=False)
    application_date = db.Column(db.Date, default=date.today)
    notes = db.Column(db.String(255))
    applied_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', backref='gradients')