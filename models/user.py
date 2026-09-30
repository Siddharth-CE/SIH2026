from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from models import db, login_manager

class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256), nullable=False)
    name = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(50), nullable=False, default='government') # 'government', 'startup', 'evaluator', 'validator', 'admin'
    title = db.Column(db.String(120))
    phone = db.Column(db.String(50))
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'), nullable=True)
    startup_id = db.Column(db.Integer, db.ForeignKey('startups.id'), nullable=True)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime, nullable=True)

    # Relationships
    department = db.relationship('Department', backref=db.backref('officers', lazy=True), foreign_keys=[department_id])
    startup = db.relationship('Startup', backref=db.backref('users', lazy=True), foreign_keys=[startup_id])

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @property
    def is_government(self):
        return self.role == 'government'

    @property
    def is_startup(self):
        return self.role == 'startup'

    @property
    def is_evaluator(self):
        return self.role == 'evaluator'

    @property
    def is_validator(self):
        return self.role == 'validator'

    @property
    def is_admin(self):
        return self.role == 'admin'

    def get_role_badge_class(self):
        mapping = {
            'government': 'badge-gov',
            'startup': 'badge-startup',
            'evaluator': 'badge-evaluator',
            'validator': 'badge-validator',
            'admin': 'badge-admin'
        }
        return mapping.get(self.role, 'badge-secondary')

    def __repr__(self):
        return f'<User {self.email} ({self.role})>'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
