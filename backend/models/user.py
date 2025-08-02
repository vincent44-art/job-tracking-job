import enum
from extensions import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

class UserRole(enum.Enum):
    CEO = "ceo"
    STOREKEEPER = "storekeeper"
    SELLER = "seller"
    PURCHASER = "purchaser"
    DRIVER = "driver"

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.Enum(UserRole), nullable=False)
    salary = db.Column(db.Numeric(10, 2), default=0.00)
    is_paid = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<User {self.email}>'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)