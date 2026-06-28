"""
Admin routes for SIET.
Handles user management, system configuration, and logs.
"""

from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from app.models import db, User, Role, Session, BehaviorLog, AnalyticsLog, Report
from app.forms.auth_forms import UserProfileForm

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')


@admin_bp.route('/')
@login_required
def admin_panel():
    """Admin panel main page."""
    if current_user.role.name != 'administrador':
        return render_template('errors/403.html', title='Acceso Denegado'), 403
    
    # Get statistics
    total_users = User.query.count()
    total_sessions = Session.query.count()
    total_behavior_logs = BehaviorLog.query.count()
    
    # Users by role
    roles = Role.query.all()
    users_by_role = {role.name: User.query.filter_by(role_id=role.id).count() for role in roles}
    
    return render_template('admin/panel.html',
                         title='Panel Administrador',
                         total_users=total_users,
                         total_sessions=total_sessions,
                         total_behavior_logs=total_behavior_logs,
                         users_by_role=users_by_role)


@admin_bp.route('/users')
@login_required
def manage_users():
    """User management page."""
    if current_user.role.name != 'administrador':
        return render_template('errors/403.html', title='Acceso Denegado'), 403
    
    users = User.query.all()
    roles = Role.query.all()
    
    return render_template('admin/users.html',
                         title='Gestión de Usuarios',
                         users=users,
                         roles=roles)


@admin_bp.route('/user/<int:user_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_user(user_id):
    """Edit user details."""
    if current_user.role.name != 'administrador':
        return render_template('errors/403.html', title='Acceso Denegado'), 403
    
    user = User.query.get_or_404(user_id)
    form = UserProfileForm(obj=user)
    
    if form.validate_on_submit():
        user.first_name = form.first_name.data
        user.last_name = form.last_name.data
        user.email = form.email.data
        
        role_id = request.form.get('role')
        if role_id:
            user.role_id = int(role_id)
        
        db.session.commit()
        flash('Usuario actualizado exitosamente.', 'success')
        return redirect(url_for('admin.manage_users'))
    
    return render_template('admin/edit_user.html', 
                         title='Editar Usuario',
                         form=form,
                         user=user,
                         roles=Role.query.all())


@admin_bp.route('/user/<int:user_id>/toggle-active', methods=['POST'])
@login_required
def toggle_user_active(user_id):
    """Toggle user active status."""
    if current_user.role.name != 'administrador':
        return jsonify({'error': 'Unauthorized'}), 403
    
    user = User.query.get_or_404(user_id)
    user.is_active = not user.is_active
    db.session.commit()
    
    return jsonify({
        'success': True,
        'is_active': user.is_active
    })


@admin_bp.route('/logs')
@login_required
def view_logs():
    """View system logs."""
    if current_user.role.name != 'administrador':
        return render_template('errors/403.html', title='Acceso Denegado'), 403
    
    # Get recent behavior logs
    behavior_logs = BehaviorLog.query.order_by(BehaviorLog.timestamp.desc()).limit(100).all()
    analytics_logs = AnalyticsLog.query.order_by(AnalyticsLog.created_at.desc()).limit(100).all()
    
    return render_template('admin/logs.html',
                         title='Logs del Sistema',
                         behavior_logs=behavior_logs,
                         analytics_logs=analytics_logs)


@admin_bp.route('/sessions')
@login_required
def manage_sessions():
    """View evaluation sessions."""
    if current_user.role.name != 'administrador':
        return render_template('errors/403.html', title='Acceso Denegado'), 403
    
    sessions = Session.query.order_by(Session.created_at.desc()).limit(50).all()
    
    return render_template('admin/sessions.html',
                         title='Sesiones de Evaluación',
                         sessions=sessions)


@admin_bp.route('/backup')
@login_required
def backup():
    """Backup database (placeholder for future implementation)."""
    if current_user.role.name != 'administrador':
        return render_template('errors/403.html', title='Acceso Denegado'), 403
    
    # In a real application, this would create a database backup
    flash('Funcionalidad de respaldo en desarrollo.', 'info')
    return render_template('admin/backup.html', title='Respaldos')
