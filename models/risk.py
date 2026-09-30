from datetime import datetime
from models import db

class Risk(db.Model):
    __tablename__ = 'risks'

    id = db.Column(db.Integer, primary_key=True)
    pilot_id = db.Column(db.Integer, db.ForeignKey('pilots.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False) # e.g. "Sensor GPS Drift in High-Density Urban Canyons"
    category = db.Column(db.String(100), default='Technical') # 'Technical', 'Operational', 'Security', 'Legal/IP', 'Integration'
    severity = db.Column(db.String(50), default='Medium') # 'Low', 'Medium', 'High', 'Critical'
    probability = db.Column(db.String(50), default='Medium') # 'Low', 'Medium', 'High'
    owner = db.Column(db.String(100), default='Department / Startup Joint')
    mitigation_strategy = db.Column(db.Text)
    status = db.Column(db.String(50), default='Open') # 'Open', 'Mitigating', 'Resolved', 'Accepted'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def get_severity_badge_class(self):
        mapping = {
            'Low': 'badge-info',
            'Medium': 'badge-warning',
            'High': 'badge-danger',
            'Critical': 'badge-critical'
        }
        return mapping.get(self.severity, 'badge-secondary')

    def get_status_badge_class(self):
        mapping = {
            'Open': 'badge-danger',
            'Mitigating': 'badge-warning',
            'Resolved': 'badge-success',
            'Accepted': 'badge-secondary'
        }
        return mapping.get(self.status, 'badge-secondary')

    def __repr__(self):
        return f'<Risk {self.title} ({self.severity})>'
