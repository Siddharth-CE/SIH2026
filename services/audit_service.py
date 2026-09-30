from flask import request
from flask_login import current_user
from models import db, AuditEvent

def log_audit_event(action, entity_type, entity_id=None, details=None, user=None):
    """
    Records an immutable audit event in SQLite database.
    """
    try:
        active_user = user or (current_user if current_user.is_authenticated else None)
        user_id = active_user.id if active_user else None
        user_email = active_user.email if active_user else 'system@govpilot.internal'
        user_role = active_user.role if active_user else 'system'

        ip = '127.0.0.1'
        if request:
            ip = request.remote_addr or '127.0.0.1'

        event = AuditEvent(
            user_id=user_id,
            user_email=user_email,
            user_role=user_role,
            action=action,
            entity_type=entity_type,
            entity_id=str(entity_id) if entity_id else None,
            ip_address=ip,
            details=details
        )
        db.session.add(event)
        db.session.commit()
        return event
    except Exception as e:
        print(f"[AUDIT LOG ERROR]: {e}")
        return None
