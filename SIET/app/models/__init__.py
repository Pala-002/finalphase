"""
Database models for SIET application.
Defines all database tables and relationships.
"""

from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class Role(db.Model):
    """User roles table."""
    __tablename__ = 'roles'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    users = db.relationship('User', backref='role', lazy='dynamic')
    
    def __repr__(self):
        return f'<Role {self.name}>'


class User(UserMixin, db.Model):
    """Users table."""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=False)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    consents = db.relationship('Consent', backref='user', lazy='dynamic')
    sessions = db.relationship('Session', backref='user', lazy='dynamic')
    redtic_answers = db.relationship('REDTICAnswer', backref='user', lazy='dynamic')
    redtic_scores = db.relationship('REDTICScore', backref='user', lazy='dynamic')
    stroop_results = db.relationship('StroopResult', backref='user', lazy='dynamic')
    nback_results = db.relationship('NBackResult', backref='user', lazy='dynamic')
    digitspan_results = db.relationship('DigitSpanResult', backref='user', lazy='dynamic')
    trailmaking_results = db.relationship('TrailMakingResult', backref='user', lazy='dynamic')
    crt_results = db.relationship('CRTResult', backref='user', lazy='dynamic')
    
    def set_password(self, password):
        """Hash and set user password."""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Check password against hash."""
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.username}>'


class Consent(db.Model):
    """Informed consent table."""
    __tablename__ = 'consent'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    accepted = db.Column(db.Boolean, nullable=False, default=False)
    ip_address = db.Column(db.String(45))
    user_agent = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Consent {self.user_id}>'


class Session(db.Model):
    """Evaluation sessions table."""
    __tablename__ = 'sessions'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    start_time = db.Column(db.DateTime, default=datetime.utcnow)
    end_time = db.Column(db.DateTime)
    total_duration_seconds = db.Column(db.Integer)
    status = db.Column(db.String(20), default='active')  # active, completed, abandoned
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    behavior_logs = db.relationship('BehaviorLog', backref='session', lazy='dynamic')
    analytics_logs = db.relationship('AnalyticsLog', backref='session', lazy='dynamic')
    
    def __repr__(self):
        return f'<Session {self.id}>'


class REDTICQuestion(db.Model):
    """RED-TIC questionnaire questions."""
    __tablename__ = 'redtic_questions'
    
    id = db.Column(db.Integer, primary_key=True)
    question_text = db.Column(db.Text, nullable=False)
    dimension = db.Column(db.String(50), nullable=False)  # fatiga, ansiedad, escepticismo, ineficacia
    reverse_scored = db.Column(db.Boolean, default=False)
    order = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    answers = db.relationship('REDTICAnswer', backref='question', lazy='dynamic')
    
    def __repr__(self):
        return f'<REDTICQuestion {self.id}>'


class REDTICAnswer(db.Model):
    """RED-TIC answers table."""
    __tablename__ = 'redtic_answers'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('redtic_questions.id'), nullable=False)
    session_id = db.Column(db.Integer, db.ForeignKey('sessions.id'))
    answer_value = db.Column(db.Integer, nullable=False)  # 1-5 Likert
    response_time_ms = db.Column(db.Integer)  # Time to answer in ms
    changed_answer = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<REDTICAnswer {self.id}>'


class REDTICScore(db.Model):
    """RED-TIC scores table."""
    __tablename__ = 'redtic_scores'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    session_id = db.Column(db.Integer, db.ForeignKey('sessions.id'))
    fatiga_tecnologica = db.Column(db.Float)
    ansiedad_tecnologica = db.Column(db.Float)
    escepticismo = db.Column(db.Float)
    ineficacia = db.Column(db.Float)
    total_score = db.Column(db.Float)
    stress_level = db.Column(db.String(20))  # bajo, moderado, alto
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<REDTICScore {self.id}>'


class StroopResult(db.Model):
    """Stroop test results."""
    __tablename__ = 'stroop_results'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    session_id = db.Column(db.Integer, db.ForeignKey('sessions.id'))
    total_trials = db.Column(db.Integer)
    correct_answers = db.Column(db.Integer)
    errors = db.Column(db.Integer)
    avg_reaction_time_ms = db.Column(db.Float)
    interference_score = db.Column(db.Float)
    completion_rate = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<StroopResult {self.id}>'


class NBackResult(db.Model):
    """N-Back test results."""
    __tablename__ = 'nback_results'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    session_id = db.Column(db.Integer, db.ForeignKey('sessions.id'))
    n_value = db.Column(db.Integer, default=2)
    total_trials = db.Column(db.Integer)
    hits = db.Column(db.Integer)
    misses = db.Column(db.Integer)
    false_alarms = db.Column(db.Integer)
    correct_rejections = db.Column(db.Integer)
    accuracy = db.Column(db.Float)
    avg_reaction_time_ms = db.Column(db.Float)
    d_prime = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<NBackResult {self.id}>'


class DigitSpanResult(db.Model):
    """Digit Span test results."""
    __tablename__ = 'digitspan_results'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    session_id = db.Column(db.Integer, db.ForeignKey('sessions.id'))
    test_type = db.Column(db.String(10))  # forward, backward
    max_span = db.Column(db.Integer)
    total_errors = db.Column(db.Integer)
    total_time_ms = db.Column(db.Integer)
    trials_completed = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<DigitSpanResult {self.id}>'


class TrailMakingResult(db.Model):
    """Trail Making Test results."""
    __tablename__ = 'trailmaking_results'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    session_id = db.Column(db.Integer, db.ForeignKey('sessions.id'))
    version = db.Column(db.String(10))  # A or B
    completion_time_ms = db.Column(db.Integer)
    errors = db.Column(db.Integer)
    completed = db.Column(db.Boolean, default=False)
    path_efficiency = db.Column(db.Float)  # Optimal path vs actual path
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<TrailMakingResult {self.id}>'


class CRTResult(db.Model):
    """Cognitive Reflection Test results."""
    __tablename__ = 'crt_results'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    session_id = db.Column(db.Integer, db.ForeignKey('sessions.id'))
    question_number = db.Column(db.Integer)
    answer_given = db.Column(db.Text)
    is_correct = db.Column(db.Boolean)
    response_time_ms = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<CRTResult {self.id}>'


class BehaviorLog(db.Model):
    """Behavioral analytics logs."""
    __tablename__ = 'behavior_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.Integer, db.ForeignKey('sessions.id'), nullable=False)
    event_type = db.Column(db.String(50), nullable=False)  # scroll, mouse_move, focus, blur, tab_change, etc.
    event_data = db.Column(db.Text)  # JSON data
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    page_url = db.Column(db.String(500))
    
    def __repr__(self):
        return f'<BehaviorLog {self.id}>'


class AnalyticsLog(db.Model):
    """Learning analytics logs."""
    __tablename__ = 'analytics_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.Integer, db.ForeignKey('sessions.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    event_type = db.Column(db.String(50), nullable=False)
    event_category = db.Column(db.String(50))  # questionnaire, cognitive_test, navigation
    duration_seconds = db.Column(db.Integer)
    clicks_count = db.Column(db.Integer, default=0)
    answer_changes = db.Column(db.Integer, default=0)
    extra_data = db.Column(db.Text)  # JSON data
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<AnalyticsLog {self.id}>'


class Report(db.Model):
    """Generated reports table."""
    __tablename__ = 'reports'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    report_type = db.Column(db.String(50), nullable=False)  # student, researcher, admin
    file_path = db.Column(db.String(500))
    generated_at = db.Column(db.DateTime, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Report {self.id}>'
