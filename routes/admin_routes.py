from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from models import db, User, Department, AuditEvent, Challenge, Startup, Pilot
from services.audit_service import log_audit_event

admin_bp = Blueprint('admin', __name__)

@admin_bp.before_request
@login_required
def ensure_admin():
    if not current_user.is_admin and not current_user.is_government:
        flash("Restricted administrative section.", "danger")
        return redirect(url_for('dashboard.index'))

@admin_bp.route('/admin/users')
def users():
    users = User.query.all()
    departments = Department.query.all()
    startups = Startup.query.all()
    return render_template('admin/users.html', users=users, departments=departments, startups=startups)


@admin_bp.route('/admin/audit-logs')
def audit_logs():
    q = AuditEvent.query
    entity_type = request.args.get('entity_type', '')
    user_email = request.args.get('user_email', '')
    query = request.args.get('q', '')

    if entity_type:
        q = q.filter_by(entity_type=entity_type)
    if user_email:
        q = q.filter_by(user_email=user_email)
    if query:
        search_term = f"%{query}%"
        q = q.filter((AuditEvent.action.ilike(search_term)) | (AuditEvent.entity_id.ilike(search_term)) | (AuditEvent.details.ilike(search_term)))

    logs = q.order_by(AuditEvent.timestamp.desc()).limit(100).all()
    entity_types = [e[0] for e in db.session.query(AuditEvent.entity_type).distinct() if e[0]]

    return render_template(
        'admin/audit.html',
        logs=logs,
        entity_types=entity_types,
        selected_entity=entity_type,
        search_query=query
    )


@admin_bp.route('/admin/departments', methods=['GET', 'POST'])
def departments():
    if request.method == 'POST':
        name = request.form.get('name')
        code = request.form.get('code')
        sector = request.form.get('sector')
        desc = request.form.get('description')
        email = request.form.get('contact_email')

        dept = Department(name=name, code=code.upper(), sector=sector, description=desc, contact_email=email)
        db.session.add(dept)
        db.session.commit()
        log_audit_event(f"Created Department {dept.name}", "Department", dept.code, sector, current_user)
        flash(f"Department '{name}' registered successfully.", "success")
        return redirect(url_for('admin.departments'))

    depts = Department.query.all()
    return render_template('admin/departments.html', departments=depts)
