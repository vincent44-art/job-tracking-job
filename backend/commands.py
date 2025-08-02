# backend/commands.py
import click
from extensions import db
from models.user import User, UserRole
from werkzeug.security import generate_password_hash
from datetime import datetime

def register_commands(app): # <- The function takes only ONE argument: 'app'
    @app.cli.command("seed_db")
    def seed_db():
        """Seeds the database with initial user data."""
        click.echo("Seeding database...")
        
        # Clear existing users to prevent duplicates
        try:
            num_deleted = db.session.query(User).delete()
            db.session.commit()
            click.echo(f"Deleted {num_deleted} existing users.")
        except Exception as e:
            db.session.rollback()
            click.echo(f"Could not clear database: {e}")
            return

        users_data = [
            {"name": "CEO Admin", "email": "ceo@fruittrack.com", "role": UserRole.CEO, "password": "password123"},
            {"name": "Sarah Storekeeper", "email": "storekeeper@company.com", "role": UserRole.STOREKEEPER, "password": "password123"},
            {"name": "John Seller", "email": "seller@company.com", "role": UserRole.SELLER, "password": "password123"},
            {"name": "Mary Purchaser", "email": "purchaser@company.com", "role": UserRole.PURCHASER, "password": "password123"},
            {"name": "David Driver", "email": "driver@company.com", "role": UserRole.DRIVER, "password": "password123"},
        ]

        for data in users_data:
            user = User(
                name=data['name'],
                email=data['email'],
                role=data['role'],
                password_hash=generate_password_hash(data['password']),
                created_at=datetime.utcnow()
            )
            db.session.add(user)

        db.session.commit()
        click.echo("Database seeding complete.")