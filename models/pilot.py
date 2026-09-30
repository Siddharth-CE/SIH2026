from datetime import datetime, date
from models import db

class Pilot(db.Model):
    __tablename__ = 'pilots'

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(50), unique=True, nullable=False) # e.g. "GP-MH-2026-00421"
    title = db.Column(db.String(250), nullable=False)
    challenge_id = db.Column(db.Integer, db.ForeignKey('challenges.id'), nullable=False)
    startup_id = db.Column(db.Integer, db.ForeignKey('startups.id'), nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'), nullable=False)
    application_id = db.Column(db.Integer, db.ForeignKey('applications.id'), nullable=True)
    assigned_officer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    assigned_validator_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)

    # Status & Timeline
    status = db.Column(db.String(50), default='active') 
    # 'active', 'at_risk', 'completed', 'extended', 'ready_for_scale', 'closed'
    duration_days = db.Column(db.Integer, default=90)
    start_date = db.Column(db.Date, default=date.today)
    end_date = db.Column(db.Date)
    
    # Financials
    total_budget = db.Column(db.Float, default=1000000.0)
    disbursed_amount = db.Column(db.Float, default=250000.0)

    # Scope & Objectives
    test_scope = db.Column(db.Text) # e.g. "10 transit buses, 5 major routes, City Zone 1 & 2"
    objectives_summary = db.Column(db.Text)
    success_criteria = db.Column(db.Text)

    # Data, IP & Compliance Section
    data_types_shared = db.Column(db.Text, default='Anonymized GPS coordinates, Bus route telemetry, Timetable metadata')
    data_access_level = db.Column(db.String(100), default='Confidential / Read-only Sandbox')
    data_retention_period = db.Column(db.String(100), default='90 Days post-pilot termination')
    data_source = db.Column(db.String(200), default='Urban Transport Command Center API')
    
    startup_ip_terms = db.Column(db.Text, default='Pre-existing ML models and algorithms remain 100% proprietary to the startup.')
    government_usage_rights = db.Column(db.Text, default='Government retains perpetual non-exclusive right to test results, data derivatives, and integration schemas.')
    joint_artifacts = db.Column(db.Text, default='Custom route mapping rules and municipal GIS layer connectors.')
    
    # Security Compliance Checklist
    sec_auth_verified = db.Column(db.Boolean, default=True)
    sec_encryption_verified = db.Column(db.Boolean, default=True)
    sec_access_control_verified = db.Column(db.Boolean, default=True)
    sec_logging_verified = db.Column(db.Boolean, default=True)
    sec_incident_process_verified = db.Column(db.Boolean, default=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    assigned_officer = db.relationship('User', foreign_keys=[assigned_officer_id])
    assigned_validator = db.relationship('User', foreign_keys=[assigned_validator_id])
    kpis = db.relationship('PilotKPI', backref='pilot', lazy=True, cascade='all, delete-orphan')
    milestones = db.relationship('PilotMilestone', backref='pilot', lazy=True, cascade='all, delete-orphan')
    payments = db.relationship('Payment', backref='pilot', lazy=True, cascade='all, delete-orphan')
    documents = db.relationship('Document', backref='pilot', lazy=True, cascade='all, delete-orphan')
    risks = db.relationship('Risk', backref='pilot', lazy=True, cascade='all, delete-orphan')
    validation_reports = db.relationship('ValidationReport', backref='pilot', lazy=True, cascade='all, delete-orphan')
    scale_decisions = db.relationship('ScaleDecision', backref='pilot', lazy=True, cascade='all, delete-orphan')

    def get_status_badge_class(self):
        mapping = {
            'active': 'badge-primary',
            'at_risk': 'badge-danger',
            'completed': 'badge-success',
            'extended': 'badge-warning',
            'ready_for_scale': 'badge-scale',
            'closed': 'badge-secondary'
        }
        return mapping.get(self.status, 'badge-secondary')

    @property
    def progress_percentage(self):
        if not self.milestones:
            return 0
        completed = sum(1 for m in self.milestones if m.status in ('Approved', 'Paid', 'Completed'))
        return int((completed / len(self.milestones)) * 100)

    def __repr__(self):
        return f'<Pilot {self.code}: {self.title}>'
