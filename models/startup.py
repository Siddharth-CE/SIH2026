from datetime import datetime
from models import db

class Startup(db.Model):
    __tablename__ = 'startups'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), unique=True, nullable=False)
    legal_name = db.Column(db.String(200))
    registration_number = db.Column(db.String(100))
    startup_recognition_number = db.Column(db.String(100)) # e.g. DPIIT/Gov recognition
    founded_year = db.Column(db.Integer)
    headquarters = db.Column(db.String(150))
    website = db.Column(db.String(200))
    contact_email = db.Column(db.String(120))
    contact_phone = db.Column(db.String(50))
    founders = db.Column(db.Text)
    employee_count = db.Column(db.String(50), default='10-50')
    summary = db.Column(db.Text)
    
    # Technology Stack & Domain
    sector = db.Column(db.String(100), default='Smart City / Transport')
    core_technology = db.Column(db.String(250)) # e.g. 'Computer Vision, Edge AI, IoT, Route Optimization'
    product_name = db.Column(db.String(150))
    product_description = db.Column(db.Text)
    architecture_overview = db.Column(db.Text)
    deployment_model = db.Column(db.String(100), default='Hybrid Cloud / On-Prem Edge')
    trl_level = db.Column(db.String(50), default='TRL 7 - System Prototype Demo') # Technology Readiness Level

    # Trust & Compliance
    cybersecurity_certified = db.Column(db.Boolean, default=True)
    cybersecurity_standard = db.Column(db.String(100), default='ISO 27001 / SOC2 Type II')
    data_residency_compliant = db.Column(db.Boolean, default=True)
    ip_ownership_clear = db.Column(db.Boolean, default=True)
    ip_details = db.Column(db.Text)
    liability_insurance = db.Column(db.Boolean, default=True)

    # Capability tags (comma-separated for matching)
    capabilities = db.Column(db.Text, default='AI, Real-time Analytics, Municipal Integration')

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    deployments = db.relationship('StartupDeployment', backref='startup', lazy=True, cascade='all, delete-orphan')
    certifications = db.relationship('StartupCertification', backref='startup', lazy=True, cascade='all, delete-orphan')
    applications = db.relationship('Application', backref='startup', lazy=True)
    pilots = db.relationship('Pilot', backref='startup', lazy=True)

    def get_capabilities_list(self):
        if not self.capabilities:
            return []
        return [c.strip() for c in self.capabilities.split(',') if c.strip()]

    def __repr__(self):
        return f'<Startup {self.name}>'


class StartupDeployment(db.Model):
    __tablename__ = 'startup_deployments'

    id = db.Column(db.Integer, primary_key=True)
    startup_id = db.Column(db.Integer, db.ForeignKey('startups.id'), nullable=False)
    client_name = db.Column(db.String(150), nullable=False)
    client_type = db.Column(db.String(100), default='Government / Municipal') # Government, Enterprise, Transit Agency
    project_title = db.Column(db.String(200), nullable=False)
    scale = db.Column(db.String(100)) # e.g. "500 IoT Nodes", "3 Municipal Zones"
    duration = db.Column(db.String(100)) # e.g. "12 Months (Completed)"
    outcome_summary = db.Column(db.Text)
    reference_contact = db.Column(db.String(150))
    year = db.Column(db.Integer, default=2025)


class StartupCertification(db.Model):
    __tablename__ = 'startup_certifications'

    id = db.Column(db.Integer, primary_key=True)
    startup_id = db.Column(db.Integer, db.ForeignKey('startups.id'), nullable=False)
    name = db.Column(db.String(150), nullable=False) # e.g. ISO 27001, CERT-In Audited, DPIIT Recognized
    issuing_body = db.Column(db.String(150))
    valid_until = db.Column(db.String(50))
    verification_url = db.Column(db.String(250))
