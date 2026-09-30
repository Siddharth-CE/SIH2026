from datetime import datetime
from models import db

class ValidationReport(db.Model):
    __tablename__ = 'validation_reports'

    id = db.Column(db.Integer, primary_key=True)
    pilot_id = db.Column(db.Integer, db.ForeignKey('pilots.id'), nullable=False)
    validator_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    report_code = db.Column(db.String(50), unique=True, nullable=False) # e.g. "VAL-GP-2026-0042"
    status = db.Column(db.String(50), default='Completed') # 'Draft', 'Completed', 'Audited'

    methodology_reviewed = db.Column(db.Text, nullable=False)
    evidence_sufficiency = db.Column(db.String(50), default='High / Sufficient') # 'High / Sufficient', 'Moderate / Partial', 'Insufficient'
    kpi_verification_summary = db.Column(db.Text, nullable=False)
    observations = db.Column(db.Text)
    limitations = db.Column(db.Text)
    conclusion = db.Column(db.Text, nullable=False)
    
    scale_recommendation = db.Column(db.String(100), default='Recommend Scale-Up Pathway')
    # 'Recommend Scale-Up Pathway', 'Recommend Pilot Extension', 'Recommend Re-testing with Modifications', 'Recommend Closure'

    verified_kpis_count = db.Column(db.Integer, default=4)
    total_kpis_count = db.Column(db.Integer, default=4)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    validator = db.relationship('User', foreign_keys=[validator_id])

    def __repr__(self):
        return f'<ValidationReport {self.report_code} for Pilot {self.pilot_id}>'
