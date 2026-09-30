from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Please log in to access this page.'
login_manager.login_message_category = 'warning'

# Import all models for easy access and table creation
from models.user import User
from models.department import Department
from models.startup import Startup, StartupDeployment, StartupCertification
from models.challenge import Challenge, EligibilityRequirement
from models.application import Application, EligibilityScreening
from models.evaluation import Evaluation, EvaluationScore
from models.pilot import Pilot
from models.kpi import PilotKPI, KPIObservation
from models.milestone import PilotMilestone
from models.payment import Payment
from models.risk import Risk
from models.document import Document
from models.validation import ValidationReport
from models.scale_decision import ScaleDecision
from models.audit import AuditEvent
from models.notification import Notification

__all__ = [
    'db',
    'login_manager',
    'User',
    'Department',
    'Startup',
    'StartupDeployment',
    'StartupCertification',
    'Challenge',
    'EligibilityRequirement',
    'Application',
    'EligibilityScreening',
    'Evaluation',
    'EvaluationScore',
    'Pilot',
    'PilotKPI',
    'KPIObservation',
    'PilotMilestone',
    'Payment',
    'Risk',
    'Document',
    'ValidationReport',
    'ScaleDecision',
    'AuditEvent',
    'Notification',
]
