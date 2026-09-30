from flask import Blueprint, render_template, request, redirect, url_for, flash, make_response, send_file
from flask_login import login_required, current_user
from models import db, Pilot, ScaleDecision, AuditEvent
from services.pdf_service import generate_scale_pack_pdf
from services.audit_service import log_audit_event
from datetime import datetime, date
import io

scale_bp = Blueprint('scale', __name__)

@scale_bp.route('/pilots/<int:pilot_id>/scale-decision', methods=['GET', 'POST'])
@login_required
def decision(pilot_id):
    pilot = Pilot.query.get_or_404(pilot_id)

    if not current_user.is_government and not current_user.is_admin:
        flash("Only authorized Government Officers can record formal scale-up decisions.", "danger")
        return redirect(url_for('pilot.passport', id=pilot_id))

    existing = ScaleDecision.query.filter_by(pilot_id=pilot.id).first()

    if request.method == 'POST':
        dec_type = request.form.get('decision_type', 'Prepare for Scale')
        pathway = request.form.get('target_procurement_pathway', '')
        reasoning = request.form.get('reasoning', '')
        notes = request.form.get('supporting_notes', '')
        signatory_name = request.form.get('authorized_signatory_name', current_user.name)
        signatory_title = request.form.get('authorized_signatory_title', current_user.title or 'Authorized Officer')
        budget = request.form.get('estimated_scale_budget', '')
        timeline = int(request.form.get('target_timeline_months', 18))

        if existing:
            sd = existing
            sd.decision_type = dec_type
            sd.target_procurement_pathway = pathway
            sd.reasoning = reasoning
            sd.supporting_notes = notes
            sd.authorized_signatory_name = signatory_name
            sd.authorized_signatory_title = signatory_title
            sd.estimated_scale_budget = budget
            sd.target_timeline_months = timeline
            sd.decision_date = date.today()
        else:
            sd = ScaleDecision(
                pilot_id=pilot.id,
                decision_maker_user_id=current_user.id,
                decision_type=dec_type,
                target_procurement_pathway=pathway,
                reasoning=reasoning,
                supporting_notes=notes,
                authorized_signatory_name=signatory_name,
                authorized_signatory_title=signatory_title,
                estimated_scale_budget=budget,
                target_timeline_months=timeline,
                decision_date=date.today()
            )
            db.session.add(sd)

        # Update pilot status
        if dec_type == 'Prepare for Scale':
            pilot.status = 'ready_for_scale'
        elif dec_type == 'Extend Pilot':
            pilot.status = 'extended'
        elif dec_type == 'Close Pilot':
            pilot.status = 'closed'

        db.session.commit()
        log_audit_event(
            f"Authorized Scale Decision: {dec_type}",
            "ScaleDecision",
            pilot.code,
            f"Signatory: {signatory_name} ({signatory_title})",
            current_user
        )
        flash(f"Scale decision '{dec_type}' has been recorded in the statutory audit register.", "success")
        return redirect(url_for('pilot.passport', id=pilot.id, tab='decision'))

    return render_template('scale/decision_form.html', pilot=pilot, decision=existing)


@scale_bp.route('/pilots/<int:pilot_id>/scale-pack')
@login_required
def pack_preview(pilot_id):
    pilot = Pilot.query.get_or_404(pilot_id)
    return render_template('scale/pack_preview.html', pilot=pilot)


@scale_bp.route('/pilots/<int:pilot_id>/scale-pack/download-pdf')
@login_required
def download_pdf(pilot_id):
    pilot = Pilot.query.get_or_404(pilot_id)
    pdf_bytes = generate_scale_pack_pdf(pilot)

    log_audit_event(
        f"Downloaded Official Scale-Up Pack (PDF)",
        "ScaleDecision",
        pilot.code,
        f"File: ScaleUp_Pack_{pilot.code}.pdf",
        current_user
    )

    response = make_response(pdf_bytes)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = f'attachment; filename=GovPilot_ScaleUp_Pack_{pilot.code}.pdf'
    return response
