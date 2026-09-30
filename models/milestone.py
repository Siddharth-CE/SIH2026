from datetime import datetime, date
from models import db

class PilotMilestone(db.Model):
    __tablename__ = 'pilot_milestones'

    id = db.Column(db.Integer, primary_key=True)
    pilot_id = db.Column(db.Integer, db.ForeignKey('pilots.id'), nullable=False)
    sequence_order = db.Column(db.Integer, default=1)
    title = db.Column(db.String(200), nullable=False) # e.g. "Milestone 1: Sensor & Model Deployment"
    description = db.Column(db.Text)
    
    due_date = db.Column(db.Date, nullable=False)
    completion_date = db.Column(db.Date, nullable=True)

    # Status: 'Pending', 'Submitted', 'Under Review', 'Approved', 'Rejected', 'Paid'
    status = db.Column(db.String(50), default='Pending')

    payment_percentage = db.Column(db.Float, default=25.0) # e.g. 25%
    payment_amount = db.Column(db.Float, default=250000.0) # e.g. 2,50,000 INR

    deliverables_summary = db.Column(db.Text)
    submission_notes = db.Column(db.Text)
    submission_document_path = db.Column(db.String(255), nullable=True)

    review_comments = db.Column(db.Text)
    reviewed_by_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    reviewed_at = db.Column(db.DateTime, nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationship to reviewer
    reviewer = db.relationship('User', foreign_keys=[reviewed_by_id])
    payments = db.relationship('Payment', backref='milestone', lazy=True, cascade='all, delete-orphan')

    def get_status_badge_class(self):
        mapping = {
            'Pending': 'badge-secondary',
            'Submitted': 'badge-warning',
            'Under Review': 'badge-info',
            'Approved': 'badge-primary',
            'Paid': 'badge-success',
            'Rejected': 'badge-danger'
        }
        return mapping.get(self.status, 'badge-secondary')

    def __repr__(self):
        return f'<Milestone {self.sequence_order}: {self.title} ({self.status})>'
