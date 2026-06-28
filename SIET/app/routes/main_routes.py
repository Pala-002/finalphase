"""
Main routes for SIET application.
Handles home page and general navigation.
"""

from flask import Blueprint, render_template
from flask_login import current_user

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    """Home page."""
    return render_template('index.html', title='SIET - Inicio')


@main_bp.route('/about')
def about():
    """About page."""
    return render_template('about.html', title='Acerca de SIET')


@main_bp.errorhandler(404)
def not_found_error(error):
    """Handle 404 errors."""
    return render_template('errors/404.html', title='Página no encontrada'), 404


@main_bp.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    return render_template('errors/500.html', title='Error interno'), 500
