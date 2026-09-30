from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from models import db, Challenge, Application, EligibilityScreening, Startup, Pilot, Document
from services.audit_service import log_audit_event
from datetime import datetime, date, timedelta

application_bp = Blueprint('application', __name__)

@application_bp.route('/applications')
@login_required
def index():
    status = request.args.get('status', '')
    challenge_id = request.args.get('challenge_id', '')

    q = Application.query
    if current_user.is_startup and current_user.startup:
        q = q.filter_by(startup_id=current_user.startup.id)
    if status:
        q = q.filter_by(status=status)
    if challenge_id:
        q = q.filter_by(challenge_id=int(challenge_id))

    applications = q.order_by(Application.created_at.desc()).all()
    challenges = Challenge.query.all()

    return render_template(
        'applications/index.html',
        applications=applications,
        challenges=challenges,
        selected_status=status,
        selected_challenge=challenge_id
    )


@application_bp.route('/challenges/<int:challenge_id>/apply', methods=['GET', 'POST'])
@login_required
def apply(challenge_id):
    challenge = Challenge.query.get_or_404(challenge_id)
    startup = current_user.startup
    if not startup and not current_user.is_admin:
        flash("You must be registered as a Startup to apply for this challenge.", "warning")
        return redirect(url_for('challenge.view', id=challenge_id))

    if not startup and current_user.is_admin:
        startup = Startup.query.first()

    existing = Application.query.filter_by(challenge_id=challenge.id, startup_id=startup.id).first()
    if existing:
        flash("You have already submitted an application for this challenge.", "info")
        return redirect(url_for('application.view', id=existing.id))

    if request.method == 'POST':
        app_count = Application.query.count() + 1
        code = f"APP-2026-{app_count:04d}"

        application = Application(
            code=code,
            challenge_id=challenge.id,
            startup_id=startup.id,
            submitted_by_user_id=current_user.id,
            status='submitted',
            
            solution_title=request.form.get('solution_title', f"Pilot Solution for {challenge.title}"),
            solution_summary=request.form.get('solution_summary', ''),
            product_readiness_trl=request.form.get('product_readiness_trl', 'TRL 7'),
            problem_alignment=request.form.get('problem_alignment', ''),
            technical_approach=request.form.get('technical_approach', ''),
            implementation_plan=request.form.get('implementation_plan', ''),
            duration_weeks=int(request.form.get('duration_weeks', 12)),
            resource_requirements=request.form.get('resource_requirements', ''),
            expected_outcomes=request.form.get('expected_outcomes', ''),
            proposed_kpis=request.form.get('proposed_kpis', ''),
            technical_specs=request.form.get('technical_specs', ''),
            data_governance_plan=request.form.get('data_governance_plan', ''),
            cloud_vs_edge=request.form.get('cloud_vs_edge', 'Hybrid Cloud Edge'),
            budget_total=request.form.get('budget_total', challenge.budget_indicative or '₹10,00,000'),
            budget_breakdown=request.form.get('budget_breakdown', ''),
            eligibility_status='pending'
        )
        db.session.add(application)
        db.session.commit()

        # Generate automated screening checklist from challenge requirements
        for req in challenge.eligibility_requirements:
            s = EligibilityScreening(
                application_id=application.id,
                criterion_name=req.criterion_title,
                is_passed=True,
                remarks="Submitted with compliance declaration"
            )
            db.session.add(s)
        db.session.commit()

        log_audit_event(f"Submitted Pilot Proposal {application.code}", "Application", application.code, f"Challenge: {challenge.code}", current_user)
        flash(f"Your application {application.code} has been successfully submitted for eligibility screening!", "success")
        return redirect(url_for('application.view', id=application.id))

    return render_template('applications/apply.html', challenge=challenge, startup=startup)


@application_bp.route('/applications/<int:id>')
@login_required
def view(id):
    application = Application.query.get_or_404(id)
    return render_template('applications/view.html', application=application)


@application_bp.route('/applications/<int:id>/screen', methods=['POST'])
@login_required
def screen_eligibility(id):
    application = Application.query.get_or_404(id)
    if not current_user.is_government and not current_user.is_admin:
        flash("Unauthorized action.", "danger")
        return redirect(url_for('application.view', id=id))

    decision = request.form.get('decision', 'verified') # 'verified', 'flagged', 'ineligible'
    notes = request.form.get('notes', '')

    application.eligibility_status = decision
    application.eligibility_notes = notes
    application.eligibility_reviewed_by_id = current_user.id
    application.eligibility_reviewed_at = datetime.utcnow()

    if decision == 'verified':
        application.status = 'in_evaluation'
    elif decision == 'flagged':
        application.status = 'eligibility_flagged'
    else:
        application.status = 'rejected'

    db.session.commit()
    log_audit_event(f"Eligibility Screening Decision: {decision.title()}", "Application", application.code, notes, current_user)
    flash(f"Eligibility decision recorded for application {application.code}.", "success")
    return redirect(url_for('application.view', id=id))


@application_bp.route('/challenges/<int:challenge_id>/comparison')
@login_required
def comparison(challenge_id):
    challenge = Challenge.query.get_or_404(challenge_id)
    applications = Application.query.filter_by(challenge_id=challenge.id).all()
    return render_template('applications/comparison.html', challenge=challenge, applications=applications)


@application_bp.route('/applications/<int:id>/select-for-pilot', methods=['POST'])
@login_required
def select_for_pilot(id):
    application = Application.query.get_or_404(id)
    if not current_user.is_government and not current_user.is_admin:
        flash("Only Government Officers can select an application for pilot execution.", "danger")
        return redirect(url_for('application.view', id=id))

    # Check if pilot already exists
    if application.pilot:
        flash("A Pilot Passport already exists for this application.", "info")
        return redirect(url_for('pilot.passport', id=application.pilot.id))

    pilot_count = Pilot.query.count() + 1
    pilot_code = f"GP-MH-2026-{pilot_count:05d}"

    pilot = Pilot(
        code=pilot_code,
        title=f"{application.startup.name}: {application.solution_title}",
        challenge_id=application.challenge_id,
        startup_id=application.startup_id,
        department_id=application.challenge.department_id,
        application_id=application.id,
        assigned_officer_id=current_user.id,
        status='active',
        duration_days=application.challenge.duration_days or 90,
        start_date=date.today(),
        end_date=date.today() + timedelta(days=(application.challenge.duration_days or 90)),
        total_budget=1000000.0,
        disbursed_amount=0.0,
        test_scope=application.challenge.geography or "Municipal Testing Corridor",
        objectives_summary=application.expected_outcomes or application.solution_summary,
        success_criteria=application.challenge.success_thresholds or "Meet target KPI thresholds."
    )
    application.status = 'pilot_selected'
    db.session.add(pilot)
    db.session.commit()

    log_audit_event(f"Selected Application & Created Pilot {pilot.code}", "Pilot", pilot.code, f"Startup: {application.startup.name}", current_user)
    flash(f"Pilot Passport {pilot.code} has been created for {application.startup.name}!", "success")
    return redirect(url_for('pilot.passport', id=pilot.id))
