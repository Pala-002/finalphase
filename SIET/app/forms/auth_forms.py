"""
WTForms for SIET application.
Handles form validation and CSRF protection.
"""

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Optional


class LoginForm(FlaskForm):
    """Login form."""
    username = StringField('Usuario', validators=[DataRequired(), Length(min=3, max=80)])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    remember_me = BooleanField('Recordarme')
    submit = SubmitField('Iniciar Sesión')


class RegistrationForm(FlaskForm):
    """Registration form."""
    username = StringField('Usuario', validators=[DataRequired(), Length(min=3, max=80)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    first_name = StringField('Nombre', validators=[Optional(), Length(max=50)])
    last_name = StringField('Apellido', validators=[Optional(), Length(max=50)])
    password = PasswordField('Contraseña', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirmar Contraseña', 
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Registrarse')


class PasswordResetRequestForm(FlaskForm):
    """Password reset request form."""
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Enviar Instrucciones')


class PasswordResetForm(FlaskForm):
    """Password reset form."""
    password = PasswordField('Nueva Contraseña', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirmar Contraseña', 
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Cambiar Contraseña')


class ConsentForm(FlaskForm):
    """Informed consent form."""
    agree = BooleanField('Acepto participar voluntariamente en este estudio', 
                        validators=[DataRequired()])
    submit = SubmitField('Aceptar y Continuar')


class UserProfileForm(FlaskForm):
    """User profile update form."""
    first_name = StringField('Nombre', validators=[Optional(), Length(max=50)])
    last_name = StringField('Apellido', validators=[Optional(), Length(max=50)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Actualizar Perfil')
