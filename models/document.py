from datetime import datetime
from models import db

class Document(db.Model):
    __tablename__ = 'documents'

    id = db.Column(db.Integer, primary_key=True)
    pilot_id = db.Column(db.Integer, db.ForeignKey('pilots.id'), nullable=True)
    challenge_id = db.Column(db.Integer, db.ForeignKey('challenges.id'), nullable=True)
    startup_id = db.Column(db.Integer, db.ForeignKey('startups.id'), nullable=True)
    
    title = db.Column(db.String(200), nullable=False)
    document_type = db.Column(db.String(100), default='General') 
    # 'Pilot Agreement', 'Startup Proposal', 'Data Sharing Agreement', 'IP Terms', 'Cybersecurity Checklist', 'Milestone Evidence', 'Validation Report', 'Scale-Up Pack'
    
    file_name = db.Column(db.String(250), nullable=False)
    file_path = db.Column(db.String(500), nullable=False)
    file_size_kb = db.Column(db.Integer, default=120)
    version = db.Column(db.String(20), default='v1.0')
    
    uploaded_by_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    status = db.Column(db.String(50), default='Verified') # 'Draft', 'Uploaded', 'Under Review', 'Verified', 'Archived'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    uploader = db.relationship('User', foreign_keys=[uploaded_by_id])

    def get_status_badge_class(self):
        mapping = {
            'Verified': 'badge-success',
            'Under Review': 'badge-warning',
            'Uploaded': 'badge-info',
            'Draft': 'badge-secondary',
            'Archived': 'badge-secondary'
        }
        return mapping.get(self.status, 'badge-secondary')

    def __repr__(self):
        return f'<Document {self.title} ({self.version})>'
