import os
from flask import Blueprint, render_template, request, redirect, url_for, flash, send_from_directory, jsonify, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from models import (
    db, Pilot, PilotKPI, KPIObservation, PilotMilestone, Payment,
    Risk, Document, ValidationReport, ScaleDecision, AuditEvent
)
from services.audit_service import log_audit_event
from datetime import datetime, date

pilot_bp = Blueprint('pilot', __name__)

@pilot_bp.route('/pilots')
@login_required
def index():
    status = request.args.get('status', '')
    sector = request.args.get('sector', '')

    q = Pilot.query
    if current_user.is_startup and current_user.startup:
        q = q.filter_by(startup_id=current_user.startup.id)
    if status:
        q = q.filter_by(status=status)

    pilots = q.order_by(Pilot.created_at.desc()).all()
    return render_template('pilots/index.html', pilots=pilots, selected_status=status, selected_sector=sector)


@pilot_bp.route('/pilots/<int:id>')
@login_required
def passport(id):
    pilot = Pilot.query.get_or_404(id)
    active_tab = request.args.get('tab', 'overview')
    audit_trail = AuditEvent.query.filter(
        (AuditEvent.entity_id == pilot.code) | 
        (AuditEvent.details.ilike(f"%{pilot.code}%"))
    ).order_by(AuditEvent.timestamp.desc()).all()

    return render_template(
        'pilots/passport.html',
        pilot=pilot,
        active_tab=active_tab,
        audit_trail=audit_trail
    )


@pilot_bp.route('/pilots/<int:id>/kpis/record', methods=['POST'])
@login_required
def record_kpi_observation(id):
    pilot = Pilot.query.get_or_404(id)
    kpi_id = request.form.get('kpi_id')
    kpi = PilotKPI.query.get_or_404(kpi_id)

    val = float(request.form.get('recorded_value', 0))
    period = request.form.get('period_label', f"Observation {len(kpi.observations) + 1}")
    note = request.form.get('evidence_note', '')

    obs = KPIObservation(
        kpi_id=kpi.id,
        recorded_value=val,
        period_label=period,
        evidence_note=note,
        verified_by_validator=True
    )
    kpi.current_value = val

    # Update status based on target
    if kpi.is_achieved:
        kpi.status = 'Target Achieved'
    else:
        kpi.status = 'On Track' if (val >= kpi.target_value * 0.85 if kpi.higher_is_better else val <= kpi.target_value * 1.25) else 'At Risk'

    db.session.add(obs)
    db.session.commit()

    log_audit_event(
        f"Recorded KPI Observation for {kpi.name}",
        "PilotKPI",
        pilot.code,
        f"New Value: {val} {kpi.unit} ({period})",
        current_user
    )
    flash(f"Observation recorded for {kpi.name}: {val} {kpi.unit}", "success")
    return redirect(url_for('pilot.passport', id=id, tab='kpis'))


@pilot_bp.route('/pilots/<int:id>/milestones/<int:m_id>/submit', methods=['POST'])
@login_required
def submit_milestone(id, m_id):
    pilot = Pilot.query.get_or_404(id)
    milestone = PilotMilestone.query.get_or_404(m_id)

    milestone.submission_notes = request.form.get('submission_notes', '')
    milestone.deliverables_summary = request.form.get('deliverables_summary', milestone.deliverables_summary)
    milestone.status = 'Under Review'
    milestone.completion_date = date.today()

    db.session.commit()
    log_audit_event(
        f"Submitted Deliverables for Milestone {milestone.sequence_order}",
        "Milestone",
        pilot.code,
        milestone.title,
        current_user
    )
    flash(f"Milestone {milestone.sequence_order} deliverables submitted for government review.", "success")
    return redirect(url_for('pilot.passport', id=id, tab='milestones'))


@pilot_bp.route('/pilots/<int:id>/milestones/<int:m_id>/review', methods=['POST'])
@login_required
def review_milestone(id, m_id):
    pilot = Pilot.query.get_or_404(id)
    milestone = PilotMilestone.query.get_or_404(m_id)

    if not current_user.is_government and not current_user.is_admin:
        flash("Unauthorized action.", "danger")
        return redirect(url_for('pilot.passport', id=id, tab='milestones'))

    decision = request.form.get('decision', 'Approved') # 'Approved', 'Rejected'
    comments = request.form.get('comments', '')

    milestone.status = decision
    milestone.review_comments = comments
    milestone.reviewed_by_id = current_user.id
    milestone.reviewed_at = datetime.utcnow()

    # If approved and payment exists, update payment to 'Department Approved'
    if decision == 'Approved':
        for pay in milestone.payments:
            if pay.status in ('Pending Milestone', 'Invoice Submitted'):
                pay.status = 'Department Approved'

    db.session.commit()
    log_audit_event(
        f"Milestone {milestone.sequence_order} {decision}",
        "Milestone",
        pilot.code,
        comments,
        current_user
    )
    flash(f"Milestone {milestone.sequence_order} has been marked {decision}.", "success")
    return redirect(url_for('pilot.passport', id=id, tab='milestones'))


@pilot_bp.route('/pilots/<int:id>/payments/<int:p_id>/disburse', methods=['POST'])
@login_required
def disburse_payment(id, p_id):
    pilot = Pilot.query.get_or_404(id)
    payment = Payment.query.get_or_404(p_id)

    if not current_user.is_government and not current_user.is_admin:
        flash("Unauthorized action.", "danger")
        return redirect(url_for('pilot.passport', id=id, tab='payments'))

    payment.status = 'Disbursed / Paid'
    payment.disbursed_at = datetime.utcnow()
    payment.transaction_reference = request.form.get('transaction_reference', f"PFMS-TXN-{datetime.now().strftime('%Y%m%d%H%M')}")
    payment.remarks = request.form.get('remarks', 'Disbursed via Treasury PFMS Gateway')

    # Update pilot disbursed total
    pilot.disbursed_amount = (pilot.disbursed_amount or 0) + payment.amount

    # Mark milestone as paid
    if payment.milestone:
        payment.milestone.status = 'Paid'

    db.session.commit()
    log_audit_event(
        f"Payment Disbursed: ₹{payment.amount:,.0f}",
        "Payment",
        payment.invoice_number,
        f"Ref: {payment.transaction_reference}",
        current_user
    )
    flash(f"Payment of ₹{payment.amount:,.0f} marked as Disbursed!", "success")
    return redirect(url_for('pilot.passport', id=id, tab='payments'))


@pilot_bp.route('/pilots/<int:id>/risks/add', methods=['POST'])
@login_required
def add_risk(id):
    pilot = Pilot.query.get_or_404(id)
    title = request.form.get('title')
    category = request.form.get('category', 'Technical')
    severity = request.form.get('severity', 'Medium')
    probability = request.form.get('probability', 'Medium')
    owner = request.form.get('owner', 'Department / Startup')
    mitigation = request.form.get('mitigation_strategy', '')

    risk = Risk(
        pilot_id=pilot.id,
        title=title or "Identified Operational Risk",
        category=category,
        severity=severity,
        probability=probability,
        owner=owner,
        mitigation_strategy=mitigation,
        status='Open'
    )
    db.session.add(risk)
    db.session.commit()

    log_audit_event(f"Logged Risk: {risk.title} ({severity})", "Risk", pilot.code, mitigation, current_user)
    flash("Risk added to register.", "info")
    return redirect(url_for('pilot.passport', id=id, tab='risks'))


@pilot_bp.route('/pilots/<int:id>/documents/upload', methods=['POST'])
@login_required
def upload_document(id):
    pilot = Pilot.query.get_or_404(id)
    doc_title = request.form.get('title', 'Pilot Supporting Document')
    doc_type = request.form.get('document_type', 'General')
    file = request.files.get('file')

    if file and file.filename:
        filename = secure_filename(file.filename)
        upload_dir = current_app.config['UPLOAD_FOLDER']
        try:
            os.makedirs(upload_dir, exist_ok=True)
        except OSError:
            pass
        file_path = os.path.join(upload_dir, filename)
        file.save(file_path)

        doc = Document(
            pilot_id=pilot.id,
            title=doc_title,
            document_type=doc_type,
            file_name=filename,
            file_path=f"uploads/{filename}",
            file_size_kb=int(os.path.getsize(file_path) / 1024),
            version="v1.0",
            uploaded_by_id=current_user.id,
            status='Verified'
        )
        db.session.add(doc)
        db.session.commit()

        log_audit_event(f"Uploaded Document: {doc_title}", "Document", pilot.code, filename, current_user)
        flash(f"Document '{filename}' uploaded successfully!", "success")
    else:
        flash("No file was selected.", "warning")

    return redirect(url_for('pilot.passport', id=id, tab='documents'))


@pilot_bp.route('/pilots/<int:id>/security/update', methods=['POST'])
@login_required
def update_security_terms(id):
    pilot = Pilot.query.get_or_404(id)
    if not current_user.is_government and not current_user.is_admin:
        flash("Unauthorized.", "danger")
        return redirect(url_for('pilot.passport', id=id, tab='data_ip'))

    pilot.data_types_shared = request.form.get('data_types_shared', pilot.data_types_shared)
    pilot.data_access_level = request.form.get('data_access_level', pilot.data_access_level)
    pilot.data_retention_period = request.form.get('data_retention_period', pilot.data_retention_period)
    pilot.startup_ip_terms = request.form.get('startup_ip_terms', pilot.startup_ip_terms)
    pilot.government_usage_rights = request.form.get('government_usage_rights', pilot.government_usage_rights)
    pilot.joint_artifacts = request.form.get('joint_artifacts', pilot.joint_artifacts)

    pilot.sec_auth_verified = bool(request.form.get('sec_auth_verified'))
    pilot.sec_encryption_verified = bool(request.form.get('sec_encryption_verified'))
    pilot.sec_access_control_verified = bool(request.form.get('sec_access_control_verified'))
    pilot.sec_logging_verified = bool(request.form.get('sec_logging_verified'))
    pilot.sec_incident_process_verified = bool(request.form.get('sec_incident_process_verified'))

    db.session.commit()
    log_audit_event("Updated Data, IP & Security Protocols", "Pilot", pilot.code, "Security parameters verified", current_user)
    flash("Data, IP and Security terms updated.", "success")
    return redirect(url_for('pilot.passport', id=id, tab='data_ip'))
