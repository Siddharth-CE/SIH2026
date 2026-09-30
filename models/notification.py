from datetime import datetime
from models import db

class Notification(db.Model):
    __tablename__ = 'notifications'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True) # None means broadcast to all users of a role
    target_role = db.Column(db.String(50), nullable=True) # 'government', 'startup', 'evaluator', 'validator', 'admin' or None
    
    title = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50), default='info') # 'info', 'success', 'warning', 'action'
    link_url = db.Column(db.String(250))
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)

    # Relationship
    user = db.relationship('User', foreign_keys=[user_id])

    def __repr__(self):
        return f'<Notification {self.title} (Read: {self.is_read})>'
