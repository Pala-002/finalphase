"""
SIET - Sistema Inteligente de Evaluación de Tecnoestrés
Main Flask Application Factory
"""

from flask import Flask
from flask_login import LoginManager
from config import config


def create_app(config_name=None):
    """Application factory for SIET."""
    if config_name is None:
        config_name = 'default'
    
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    from app.models import db
    db.init_app(app)
    
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Por favor inicia sesión para acceder.'
    login_manager.login_message_category = 'warning'
    
    @login_manager.user_loader
    def load_user(user_id):
        from app.models import User
        return User.query.get(int(user_id))
    
    # Register blueprints
    from app.routes import auth_bp, main_bp, evaluation_bp, cognitive_bp, dashboard_bp, admin_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(evaluation_bp)
    app.register_blueprint(cognitive_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(admin_bp)
    
    # Create database tables and initialize data
    with app.app_context():
        from app.services.initializer import initialize_database
        initialize_database()
    
    return app
