"""Routes module initialization."""

from app.routes.auth_routes import auth_bp
from app.routes.main_routes import main_bp
from app.routes.evaluation_routes import evaluation_bp
from app.routes.cognitive_routes import cognitive_bp
from app.routes.dashboard_routes import dashboard_bp
from app.routes.admin_routes import admin_bp

__all__ = ['auth_bp', 'main_bp', 'evaluation_bp', 'cognitive_bp', 'dashboard_bp', 'admin_bp']
