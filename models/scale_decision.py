from datetime import datetime, date
from models import db

class ScaleDecision(db.Model):
    __tablename__ = 'scale_decisions'

    id = db.Column(db.Integer, primary_key=True)
    pilot_id = db.Column(db.Integer, db.ForeignKey('pilots.id'), nullable=False)
    decision_maker_user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    # Decision Type: 'Prepare for Scale', 'Extend Pilot', 'Modify & Re-test', 'Close Pilot'
    decision_type = db.Column(db.String(100), nullable=False, default='Prepare for Scale')
    
    target_procurement_pathway = db.Column(db.String(250), default='Rule 149 Innovation Procurement / Open Competitive RFP with Pilot Pre-qualification')
    reasoning = db.Column(db.Text, nullable=False)
    supporting_notes = db.Column(db.Text)
    
    authorized_signatory_name = db.Column(db.String(150), nullable=False)
    authorized_signatory_title = db.Column(db.String(150), nullable=False)
    decision_date = db.Column(db.Date, default=date.today)

    estimated_scale_budget = db.Column(db.String(100), default='₹1,80,00,000 (Pan-City 250 Buses)')
    target_timeline_months = db.Column(db.Integer, default=18)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    decision_maker = db.relationship('User', foreign_keys=[decision_maker_user_id])

    def get_decision_badge_class(self):
        mapping = {
            'Prepare for Scale': 'badge-scale',
            'Extend Pilot': 'badge-warning',
            'Modify & Re-test': 'badge-info',
            'Close Pilot': 'badge-secondary'
        }
        return mapping.get(self.decision_type, 'badge-secondary')

    def __repr__(self):
        return f'<ScaleDecision {self.decision_type} for Pilot {self.pilot_id}>'
