from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models import db, Pilot, ValidationReport, PilotKPI
from services.audit_service import log_audit_event
from datetime import datetime

validation_bp = Blueprint('validation', __name__)

@validation_bp.route('/validation')
@login_required
def index():
    pilots = Pilot.query.all()
    reports = ValidationReport.query.order_by(ValidationReport.created_at.desc()).all()
    return render_template('validation/index.html', pilots=pilots, reports=reports)


@validation_bp.route('/validation/pilots/<int:pilot_id>/create', methods=['GET', 'POST'])
@login_required
def create_report(pilot_id):
    pilot = Pilot.query.get_or_404(pilot_id)

    if not current_user.is_validator and not current_user.is_admin:
        flash("Only authorized Independent Validators can submit validation dossiers.", "danger")
        return redirect(url_for('pilot.passport', id=pilot_id))

    existing = ValidationReport.query.filter_by(pilot_id=pilot.id).first()

    if request.method == 'POST':
        methodology = request.form.get('methodology_reviewed', '')
        sufficiency = request.form.get('evidence_sufficiency', 'High / Sufficient')
        kpi_summary = request.form.get('kpi_verification_summary', '')
        observations = request.form.get('observations', '')
        limitations = request.form.get('limitations', '')
        conclusion = request.form.get('conclusion', '')
        recommendation = request.form.get('scale_recommendation', 'Recommend Scale-Up Pathway')

        rep_count = ValidationReport.query.count() + 1
        code = f"VAL-GP-2026-{rep_count:04d}"

        if existing:
            report = existing
            report.methodology_reviewed = methodology
            report.evidence_sufficiency = sufficiency
            report.kpi_verification_summary = kpi_summary
            report.observations = observations
            report.limitations = limitations
            report.conclusion = conclusion
            report.scale_recommendation = recommendation
            report.submitted_at = datetime.utcnow()
        else:
            report = ValidationReport(
                pilot_id=pilot.id,
                validator_id=current_user.id,
                report_code=code,
                status='Completed',
                methodology_reviewed=methodology,
                evidence_sufficiency=sufficiency,
                kpi_verification_summary=kpi_summary,
                observations=observations,
                limitations=limitations,
                conclusion=conclusion,
                scale_recommendation=recommendation,
                verified_kpis_count=len(pilot.kpis),
                total_kpis_count=len(pilot.kpis),
                submitted_at=datetime.utcnow()
            )
            db.session.add(report)

        # Update pilot status to ready_for_scale if recommended
        if 'Scale' in recommendation:
            pilot.status = 'ready_for_scale'

        db.session.commit()
        log_audit_event(
            f"Submitted Independent Validation Report {report.report_code}",
            "ValidationReport",
            pilot.code,
            f"Recommendation: {recommendation}",
            current_user
        )
        flash(f"Validation Report {report.report_code} has been officially recorded!", "success")
        return redirect(url_for('pilot.passport', id=pilot.id, tab='validation'))

    return render_template('validation/report_form.html', pilot=pilot, report=existing)
