"""
Configuration module for SIET application.
Contains all configuration settings, thresholds, and constants.
"""

import os
from datetime import timedelta

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    """Base configuration class."""
    
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'siet-secret-key-change-in-production'
    
    # Database configuration
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        f'sqlite:///{os.path.join(BASE_DIR, "database", "siet.db")}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Session configuration
    PERMANENT_SESSION_LIFETIME = timedelta(hours=2)
    
    # Security
    WTF_CSRF_ENABLED = True
    
    # RED-TIC Thresholds (centralized for future validation)
    REDTIC_THRESHOLDS = {
        'fatiga_tecnologica': {'min': 0, 'max': 100},
        'ansiedad_tecnologica': {'min': 0, 'max': 100},
        'escepticismo': {'min': 0, 'max': 100},
        'ineficacia': {'min': 0, 'max': 100},
    }
    
    # Stress level classification thresholds
    STRESS_LEVELS = {
        'bajo': {'min': 0, 'max': 33},
        'moderado': {'min': 34, 'max': 66},
        'alto': {'min': 67, 'max': 100}
    }
    
    # Cognitive test configurations
    COGNITIVE_TESTS = {
        'stroop': {
            'trials': 20,
            'max_time_ms': 2000
        },
        'nback': {
            'n': 2,
            'trials': 20,
            'stimulus_time_ms': 500,
            'response_time_ms': 2500
        },
        'digitspan': {
            'initial_length': 3,
            'max_length': 9,
            'attempts_per_level': 2
        },
        'trailmaking': {
            'version_a': True,
            'version_b': True
        },
        'crt': {
            'questions': 3
        }
    }
    
    # Likert scale options
    LIKERT_SCALE = [
        {'value': 1, 'label': 'Nunca'},
        {'value': 2, 'label': 'Rara vez'},
        {'value': 3, 'label': 'Algunas veces'},
        {'value': 4, 'label': 'Frecuentemente'},
        {'value': 5, 'label': 'Siempre'}
    ]


class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True


class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
