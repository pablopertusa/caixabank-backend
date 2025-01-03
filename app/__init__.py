from flask import Flask
from flask_jwt_extended import JWTManager
from app.config import Config
from app.models import db

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    with app.app_context():
        db.create_all()
    JWTManager(app)

    # Register blueprints
    from app.routes.auth import auth_bp
    from app.routes.recurring_expenses import expenses_bp
    from app.routes.tranfers import transfers_bp
    from app.routes.alerts import alerts_bp
    from app.routes.transactions import transactions_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(expenses_bp)
    app.register_blueprint(transfers_bp)
    app.register_blueprint(alerts_bp)
    app.register_blueprint(transactions_bp)

    return app
