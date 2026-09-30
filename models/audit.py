from datetime import datetime
from models import db

class AuditEvent(db.Model):
    __tablename__ = 'audit_events'

    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    user_email = db.Column(db.String(120))
    user_role = db.Column(db.String(50))
    
    action = db.Column(db.String(150), nullable=False) # e.g. "Published Challenge", "Submitted Proposal", "Recorded Evaluation"
    entity_type = db.Column(db.String(100), nullable=False) # "Challenge", "Application", "Evaluation", "Pilot", "Milestone", "ScaleDecision"
    entity_id = db.Column(db.String(100)) # e.g. "CH-TRANS-2026-001" or pilot ID
    ip_address = db.Column(db.String(50), default='127.0.0.1')
    details = db.Column(db.Text)

    # Relationships
    user = db.relationship('User', foreign_keys=[user_id])

    def __repr__(self):
        return f'<AuditEvent {self.timestamp.strftime("%Y-%m-%d %H:%M")} - {self.action}>'
