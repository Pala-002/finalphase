"""
Authentication routes for SIET.
Handles login, logout, registration, and password recovery.
"""

from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app.models import db, User, Role
from app.forms.auth_forms import LoginForm, RegistrationForm, PasswordResetRequestForm, PasswordResetForm

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Handle user login."""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.student_dashboard'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next')
            
            # Redirect based on role
            if not next_page or next_page == 'None':
                if user.role.name == 'administrador':
                    next_page = url_for('admin.admin_panel')
                elif user.role.name == 'investigador':
                    next_page = url_for('dashboard.researcher_dashboard')
                else:
                    next_page = url_for('dashboard.student_dashboard')
            
            flash('Inicio de sesión exitoso.', 'success')
            return redirect(next_page)
        
        flash('Usuario o contraseña incorrectos.', 'error')
    
    return render_template('auth/login.html', form=form, title='Iniciar Sesión')


@auth_bp.route('/logout')
@login_required
def logout():
    """Handle user logout."""
    logout_user()
    flash('Sesión cerrada correctamente.', 'info')
    return redirect(url_for('auth.login'))


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """Handle user registration."""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.student_dashboard'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        # Check if user exists
        existing_user = User.query.filter(
            (User.username == form.username.data) | 
            (User.email == form.email.data)
        ).first()
        
        if existing_user:
            flash('El usuario o email ya está registrado.', 'error')
            return render_template('auth/register.html', form=form, title='Registro')
        
        # Get student role by default
        student_role = Role.query.filter_by(name='estudiante').first()
        if not student_role:
            # Create default roles if they don't exist
            from app.services.initializer import create_default_roles
            create_default_roles()
            student_role = Role.query.filter_by(name='estudiante').first()
        
        user = User(
            username=form.username.data,
            email=form.email.data,
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            role_id=student_role.id
        )
        user.set_password(form.password.data)
        
        db.session.add(user)
        db.session.commit()
        
        flash('Registro exitoso. Por favor inicia sesión.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/register.html', form=form, title='Registro')


@auth_bp.route('/reset-password', methods=['GET', 'POST'])
def reset_password_request():
    """Handle password reset request."""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.student_dashboard'))
    
    form = PasswordResetRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        
        if user:
            # In a real application, send email with reset token
            # For prototype, just show success message
            flash('Se han enviado instrucciones para restablecer tu contraseña.', 'info')
            return redirect(url_for('auth.login'))
        
        flash('Email no encontrado.', 'error')
    
    return render_template('auth/reset_password_request.html', form=form, title='Recuperar Contraseña')


@auth_bp.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    """Handle password reset with token."""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.student_dashboard'))
    
    # In a real application, validate token here
    # For prototype, skip token validation
    
    form = PasswordResetForm()
    if form.validate_on_submit():
        # In a real application, decode token to get user
        # For prototype, this is a simplified version
        flash('Contraseña restablecida exitosamente.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/reset_password.html', form=form, title='Nueva Contraseña')


@auth_bp.route('/profile')
@login_required
def profile():
    """Display user profile."""
    return render_template('auth/profile.html', title='Mi Perfil')
