from datetime import datetime
from models import db

class Department(db.Model):
    __tablename__ = 'departments'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), unique=True, nullable=False)
    code = db.Column(db.String(20), unique=True, nullable=False)
    sector = db.Column(db.String(100), nullable=False) # Transport, Water, Infrastructure, Waste, Healthcare, Education, etc.
    description = db.Column(db.Text)
    contact_email = db.Column(db.String(120))
    jurisdiction = db.Column(db.String(120), default='State/Municipal')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    challenges = db.relationship('Challenge', backref='department', lazy=True)
    pilots = db.relationship('Pilot', backref='department', lazy=True)

    def __repr__(self):
        return f'<Department {self.name} ({self.code})>'
