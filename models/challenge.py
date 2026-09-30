from datetime import datetime
from models import db

class Challenge(db.Model):
    __tablename__ = 'challenges'

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(50), unique=True, nullable=False) # e.g. "CH-TRANS-2026-001"
    title = db.Column(db.String(250), nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'), nullable=False)
    sector = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(50), default='draft') # 'draft', 'published', 'in_evaluation', 'pilot_active', 'completed', 'archived'

    # Step 1: Problem Definition
    problem_summary = db.Column(db.Text, nullable=False)
    problem_details = db.Column(db.Text)
    urgency_level = db.Column(db.String(50), default='High')

    # Step 2: Current State
    baseline_summary = db.Column(db.Text)
    current_process = db.Column(db.Text)
    pain_points = db.Column(db.Text)
    affected_users = db.Column(db.String(250))

    # Step 3: Desired Outcome
    expected_outcome = db.Column(db.Text, nullable=False)
    target_improvement = db.Column(db.String(250))
    target_kpis_summary = db.Column(db.Text)

    # Step 4: Pilot Scope
    geography = db.Column(db.String(250))
    target_users_count = db.Column(db.String(100))
    test_facilities = db.Column(db.String(250))
    duration_days = db.Column(db.Integer, default=90)
    budget_indicative = db.Column(db.String(100), default='₹10,00,000')

    # Step 5: Data & Integration
    available_datasets = db.Column(db.Text)
    data_sensitivity = db.Column(db.String(100), default='Confidential / Anonymized Government Data')
    api_availability = db.Column(db.String(100), default='REST APIs Available with API Key')
    data_access_terms = db.Column(db.Text)

    # Step 6: Technical Constraints & Security
    technical_constraints = db.Column(db.Text)
    security_requirements = db.Column(db.Text)
    integration_requirements = db.Column(db.Text)

    # Step 7: Evaluation & Success
    evaluation_criteria_notes = db.Column(db.Text)
    success_thresholds = db.Column(db.Text)

    # Metadata & Dates
    created_by_user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    published_at = db.Column(db.DateTime, nullable=True)
    application_deadline = db.Column(db.DateTime, nullable=True)

    # Relationships
    author = db.relationship('User', foreign_keys=[created_by_user_id])
    eligibility_requirements = db.relationship('EligibilityRequirement', backref='challenge', lazy=True, cascade='all, delete-orphan')
    applications = db.relationship('Application', backref='challenge', lazy=True)
    pilots = db.relationship('Pilot', backref='challenge', lazy=True)

    @property
    def application_count(self):
        return len(self.applications)

    def get_status_badge_class(self):
        mapping = {
            'draft': 'badge-draft',
            'published': 'badge-published',
            'in_evaluation': 'badge-eval',
            'pilot_active': 'badge-pilot',
            'completed': 'badge-success',
            'archived': 'badge-secondary'
        }
        return mapping.get(self.status, 'badge-secondary')

    def __repr__(self):
        return f'<Challenge {self.code}: {self.title}>'


class EligibilityRequirement(db.Model):
    __tablename__ = 'eligibility_requirements'

    id = db.Column(db.Integer, primary_key=True)
    challenge_id = db.Column(db.Integer, db.ForeignKey('challenges.id'), nullable=False)
    criterion_title = db.Column(db.String(250), nullable=False)
    description = db.Column(db.Text)
    is_mandatory = db.Column(db.Boolean, default=True)
    requirement_type = db.Column(db.String(100), default='Standard') # 'Recognition', 'Technical', 'Compliance', 'Experience'
