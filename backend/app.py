from flask import Flask
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from config import Config
from commands import register_commands
from extensions import db

# Initialize extensions
migrate = Migrate()
jwt = JWTManager()
cors = CORS()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions with the app
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    cors.init_app(app)

    # Import and register blueprints
    from routes.auth import auth_bp
    from routes.user import user_bp
    from routes.inventory import inventory_bp
    from routes.sales import sales_bp
    from routes.purchases import purchases_bp
    from routes.stock import stock_bp
    from routes.gradients import gradients_bp
    from routes.messages import messages_bp
    from routes.dashboard import dashboard_bp

    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(user_bp, url_prefix='/api/users')
    app.register_blueprint(inventory_bp, url_prefix='/api/inventory')
    app.register_blueprint(sales_bp, url_prefix='/api/sales')
    app.register_blueprint(purchases_bp, url_prefix='/api/purchases')
    app.register_blueprint(stock_bp, url_prefix='/api/stock')
    app.register_blueprint(gradients_bp, url_prefix='/api/gradients')
    app.register_blueprint(messages_bp, url_prefix='/api/messages')
    app.register_blueprint(dashboard_bp, url_prefix='/api/dashboard')

    register_commands(app)

    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)