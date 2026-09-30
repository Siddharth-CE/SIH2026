from datetime import datetime, date
from models import db

class PilotKPI(db.Model):
    __tablename__ = 'pilot_kpis'

    id = db.Column(db.Integer, primary_key=True)
    pilot_id = db.Column(db.Integer, db.ForeignKey('pilots.id'), nullable=False)
    name = db.Column(db.String(150), nullable=False) # e.g. "Average Passenger Waiting Time"
    description = db.Column(db.Text)
    
    baseline_value = db.Column(db.Float, nullable=False) # e.g. 16.0
    target_value = db.Column(db.Float, nullable=False)   # e.g. 12.0
    current_value = db.Column(db.Float, nullable=False)  # e.g. 10.8
    unit = db.Column(db.String(50), default='minutes')    # e.g. "min", "%", "hours", "per km"
    higher_is_better = db.Column(db.Boolean, default=False) # False for waiting time/errors, True for accuracy/adherence

    data_source = db.Column(db.String(150), default='Automated Telemetry & Passenger Survey')
    measurement_method = db.Column(db.String(200), default='Real-time GPS timestamp delta at bus stops')
    frequency = db.Column(db.String(50), default='Weekly')
    success_threshold = db.Column(db.String(150), default='Improvement > 25% over baseline')

    status = db.Column(db.String(50), default='On Track') # 'Target Achieved', 'On Track', 'At Risk', 'Pending Data'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    observations = db.relationship('KPIObservation', backref='kpi', lazy=True, cascade='all, delete-orphan', order_by='KPIObservation.observation_date')

    @property
    def is_achieved(self):
        if self.higher_is_better:
            return self.current_value >= self.target_value
        else:
            return self.current_value <= self.target_value

    def get_status_badge_class(self):
        mapping = {
            'Target Achieved': 'badge-success',
            'On Track': 'badge-info',
            'At Risk': 'badge-danger',
            'Pending Data': 'badge-secondary'
        }
        return mapping.get(self.status, 'badge-secondary')

    def __repr__(self):
        return f'<PilotKPI {self.name}: {self.current_value} {self.unit}>'


class KPIObservation(db.Model):
    __tablename__ = 'kpi_observations'

    id = db.Column(db.Integer, primary_key=True)
    kpi_id = db.Column(db.Integer, db.ForeignKey('pilot_kpis.id'), nullable=False)
    observation_date = db.Column(db.Date, default=date.today)
    recorded_value = db.Column(db.Float, nullable=False)
    period_label = db.Column(db.String(50)) # e.g. "Week 1", "Week 2", "Baseline"
    evidence_note = db.Column(db.Text)
    verified_by_validator = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
