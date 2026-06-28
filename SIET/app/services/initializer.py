"""
Services module for SIET.
Contains business logic and initialization services.
"""

from app.models import db, Role, User


def create_default_roles():
    """Create default roles if they don't exist."""
    default_roles = [
        {'name': 'administrador', 'description': 'Administrador del sistema'},
        {'name': 'investigador', 'description': 'Investigador con acceso a analytics'},
        {'name': 'estudiante', 'description': 'Estudiante que realiza evaluaciones'}
    ]
    
    for role_data in default_roles:
        existing_role = Role.query.filter_by(name=role_data['name']).first()
        if not existing_role:
            role = Role(
                name=role_data['name'],
                description=role_data['description']
            )
            db.session.add(role)
    
    db.session.commit()


def create_admin_user(username='admin', email='admin@siet.local', password='admin123'):
    """Create default admin user if it doesn't exist."""
    admin_role = Role.query.filter_by(name='administrador').first()
    
    if not admin_role:
        create_default_roles()
        admin_role = Role.query.filter_by(name='administrador').first()
    
    existing_user = User.query.filter_by(username=username).first()
    if not existing_user:
        admin = User(
            username=username,
            email=email,
            first_name='Administrador',
            last_name='SIET',
            role_id=admin_role.id,
            is_active=True
        )
        admin.set_password(password)
        db.session.add(admin)
        db.session.commit()
        return True
    
    return False


def initialize_database():
    """Initialize database with tables and default data."""
    # Create all tables
    db.create_all()
    
    # Create default roles
    create_default_roles()
    
    # Create admin user
    create_admin_user()
    
    print("Database initialized successfully!")
    print("Default admin user created:")
    print("  Username: admin")
    print("  Password: admin123")
    print("  Email: admin@siet.local")
