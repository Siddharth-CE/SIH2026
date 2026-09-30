from datetime import datetime
from models import db

class Payment(db.Model):
    __tablename__ = 'payments'

    id = db.Column(db.Integer, primary_key=True)
    pilot_id = db.Column(db.Integer, db.ForeignKey('pilots.id'), nullable=False)
    milestone_id = db.Column(db.Integer, db.ForeignKey('pilot_milestones.id'), nullable=False)
    
    invoice_number = db.Column(db.String(100), unique=True, nullable=False) # e.g. "INV-GP-2026-001"
    amount = db.Column(db.Float, nullable=False)
    currency = db.Column(db.String(10), default='INR (₹)')
    
    # Status: 'Pending Milestone', 'Invoice Submitted', 'Department Approved', 'Disbursed / Paid'
    status = db.Column(db.String(50), default='Pending Milestone')

    disbursed_at = db.Column(db.DateTime, nullable=True)
    transaction_reference = db.Column(db.String(100))
    remarks = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def get_status_badge_class(self):
        mapping = {
            'Pending Milestone': 'badge-secondary',
            'Invoice Submitted': 'badge-warning',
            'Department Approved': 'badge-primary',
            'Disbursed / Paid': 'badge-success'
        }
        return mapping.get(self.status, 'badge-secondary')

    def __repr__(self):
        return f'<Payment {self.invoice_number}: {self.amount} ({self.status})>'
