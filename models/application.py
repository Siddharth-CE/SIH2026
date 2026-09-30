from datetime import datetime
from models import db

class Application(db.Model):
    __tablename__ = 'applications'

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(50), unique=True, nullable=False) # e.g. "APP-2026-0042"
    challenge_id = db.Column(db.Integer, db.ForeignKey('challenges.id'), nullable=False)
    startup_id = db.Column(db.Integer, db.ForeignKey('startups.id'), nullable=False)
    submitted_by_user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Status & Workflow
    status = db.Column(db.String(50), default='submitted') 
    # 'submitted', 'eligibility_passed', 'eligibility_flagged', 'in_evaluation', 'shortlisted', 'pilot_selected', 'rejected'

    # Step 1: Solution Overview
    solution_title = db.Column(db.String(250), nullable=False)
    solution_summary = db.Column(db.Text, nullable=False)
    product_readiness_trl = db.Column(db.String(50), default='TRL 7')

    # Step 2: Problem Alignment & Approach
    problem_alignment = db.Column(db.Text, nullable=False)
    technical_approach = db.Column(db.Text, nullable=False)

    # Step 3: Implementation & Scope
    implementation_plan = db.Column(db.Text)
    duration_weeks = db.Column(db.Integer, default=12)
    resource_requirements = db.Column(db.Text)

    # Step 4: Expected Outcomes & KPIs
    expected_outcomes = db.Column(db.Text)
    proposed_kpis = db.Column(db.Text)

    # Step 5: Technical, Security & Data Specs
    technical_specs = db.Column(db.Text)
    data_governance_plan = db.Column(db.Text)
    cloud_vs_edge = db.Column(db.String(100), default='Hybrid Cloud Edge')

    # Step 6: Budget & Commercials
    budget_total = db.Column(db.String(100), default='₹8,50,000')
    budget_breakdown = db.Column(db.Text)

    # Eligibility Screening
    eligibility_status = db.Column(db.String(50), default='pending') # 'pending', 'verified', 'flagged', 'ineligible'
    eligibility_notes = db.Column(db.Text)
    eligibility_reviewed_by_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    eligibility_reviewed_at = db.Column(db.DateTime, nullable=True)

    # Overall Calculated Evaluation Score
    average_score = db.Column(db.Float, default=0.0)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    submitted_by = db.relationship('User', foreign_keys=[submitted_by_user_id])
    eligibility_reviewer = db.relationship('User', foreign_keys=[eligibility_reviewed_by_id])
    screening_items = db.relationship('EligibilityScreening', backref='application', lazy=True, cascade='all, delete-orphan')
    evaluations = db.relationship('Evaluation', backref='application', lazy=True, cascade='all, delete-orphan')
    pilot = db.relationship('Pilot', backref='source_application', uselist=False, lazy=True)

    def get_status_badge_class(self):
        mapping = {
            'submitted': 'badge-warning',
            'eligibility_passed': 'badge-info',
            'eligibility_flagged': 'badge-danger',
            'in_evaluation': 'badge-eval',
            'shortlisted': 'badge-primary',
            'pilot_selected': 'badge-success',
            'rejected': 'badge-secondary'
        }
        return mapping.get(self.status, 'badge-secondary')

    def __repr__(self):
        return f'<Application {self.code} - Startup {self.startup_id}>'


class EligibilityScreening(db.Model):
    __tablename__ = 'eligibility_screenings'

    id = db.Column(db.Integer, primary_key=True)
    application_id = db.Column(db.Integer, db.ForeignKey('applications.id'), nullable=False)
    criterion_name = db.Column(db.String(200), nullable=False) # e.g. "Startup Recognition", "Cybersecurity Document", "Relevant Capability"
    is_passed = db.Column(db.Boolean, default=True)
    remarks = db.Column(db.String(250))
