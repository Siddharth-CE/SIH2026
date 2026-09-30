from datetime import datetime
from models import db

class Evaluation(db.Model):
    __tablename__ = 'evaluations'

    id = db.Column(db.Integer, primary_key=True)
    application_id = db.Column(db.Integer, db.ForeignKey('applications.id'), nullable=False)
    evaluator_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # 6 Standard GovPilot Evaluation Criteria (0-100 scale each)
    technical_feasibility_score = db.Column(db.Float, default=0.0) # 25% weight
    technical_feasibility_comment = db.Column(db.Text)

    expected_outcome_score = db.Column(db.Float, default=0.0) # 25% weight
    expected_outcome_comment = db.Column(db.Text)

    scalability_score = db.Column(db.Float, default=0.0) # 15% weight
    scalability_comment = db.Column(db.Text)

    security_risk_score = db.Column(db.Float, default=0.0) # 15% weight
    security_risk_comment = db.Column(db.Text)

    implementation_readiness_score = db.Column(db.Float, default=0.0) # 10% weight
    implementation_readiness_comment = db.Column(db.Text)

    cost_value_score = db.Column(db.Float, default=0.0) # 10% weight
    cost_value_comment = db.Column(db.Text)

    # Calculated Total Weighted Score (0 to 100)
    total_weighted_score = db.Column(db.Float, default=0.0)

    # Governance & Conflict of Interest
    conflict_of_interest_cleared = db.Column(db.Boolean, default=False)
    coi_declaration_text = db.Column(db.String(250), default="I confirm that I have no conflict of interest in this evaluation.")

    # Status
    status = db.Column(db.String(50), default='draft') # 'draft', 'submitted'
    overall_recommendation = db.Column(db.String(50), default='Recommend with Standard Oversight') # 'Strongly Recommend', 'Recommend with Standard Oversight', 'Conditional', 'Do Not Recommend'
    general_remarks = db.Column(db.Text)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    submitted_at = db.Column(db.DateTime, nullable=True)

    # Relationships
    evaluator = db.relationship('User', foreign_keys=[evaluator_id], backref='evaluations_given')
    scores = db.relationship('EvaluationScore', backref='evaluation', lazy=True, cascade='all, delete-orphan')

    def calculate_weighted_score(self):
        weighted = (
            (self.technical_feasibility_score or 0) * 0.25 +
            (self.expected_outcome_score or 0) * 0.25 +
            (self.scalability_score or 0) * 0.15 +
            (self.security_risk_score or 0) * 0.15 +
            (self.implementation_readiness_score or 0) * 0.10 +
            (self.cost_value_score or 0) * 0.10
        )
        self.total_weighted_score = round(weighted, 1)
        return self.total_weighted_score

    def __repr__(self):
        return f'<Evaluation {self.id} for App {self.application_id} by Evaluator {self.evaluator_id}>'


class EvaluationScore(db.Model):
    __tablename__ = 'evaluation_scores'

    id = db.Column(db.Integer, primary_key=True)
    evaluation_id = db.Column(db.Integer, db.ForeignKey('evaluations.id'), nullable=False)
    criteria_name = db.Column(db.String(100), nullable=False)
    weight_percentage = db.Column(db.Float, nullable=False)
    score = db.Column(db.Float, nullable=False)
    comments = db.Column(db.Text)
