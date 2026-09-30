from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from models import db, Challenge, Department, EligibilityRequirement, Application
from services.ai_service import generate_challenge_blueprint
from services.matching_service import match_startups_for_challenge
from services.audit_service import log_audit_event
from datetime import datetime, timedelta

challenge_bp = Blueprint('challenge', __name__)

@challenge_bp.route('/challenges')
def index():
    sector = request.args.get('sector', '')
    status = request.args.get('status', '')
    dept_id = request.args.get('department_id', '')
    query = request.args.get('q', '')

    q = Challenge.query
    if sector:
        q = q.filter(Challenge.sector == sector)
    if status:
        q = q.filter(Challenge.status == status)
    if dept_id:
        q = q.filter(Challenge.department_id == int(dept_id))
    if query:
        search_term = f"%{query}%"
        q = q.filter((Challenge.title.ilike(search_term)) | (Challenge.code.ilike(search_term)) | (Challenge.problem_summary.ilike(search_term)))

    challenges = q.order_by(Challenge.created_at.desc()).all()
    departments = Department.query.all()
    sectors = [d[0] for d in db.session.query(Department.sector).distinct() if d[0]]

    return render_template(
        'challenges/index.html',
        challenges=challenges,
        departments=departments,
        sectors=sectors,
        selected_sector=sector,
        selected_status=status,
        selected_dept=dept_id,
        search_query=query
    )


@challenge_bp.route('/challenges/<int:id>')
def view(id):
    challenge = Challenge.query.get_or_404(id)
    suggested_startups = match_startups_for_challenge(challenge=challenge)
    existing_application = None
    if current_user.is_authenticated and current_user.is_startup and current_user.startup:
        existing_application = Application.query.filter_by(challenge_id=challenge.id, startup_id=current_user.startup.id).first()

    return render_template(
        'challenges/view.html',
        challenge=challenge,
        suggested_startups=suggested_startups,
        existing_application=existing_application
    )


@challenge_bp.route('/challenges/builder', methods=['GET', 'POST'])
@login_required
def builder():
    if not current_user.is_government and not current_user.is_admin:
        flash("Only authorized Government Officers can create challenges.", "danger")
        return redirect(url_for('challenge.index'))

    departments = Department.query.all()

    if request.method == 'POST':
        title = request.form.get('title')
        dept_id = request.form.get('department_id')
        sector = request.form.get('sector')
        problem_summary = request.form.get('problem_summary')
        expected_outcome = request.form.get('expected_outcome')
        is_publish = request.form.get('action') == 'publish'

        count = Challenge.query.count() + 1
        code = f"CH-{(sector[:5] if sector else 'GOV').upper()}-2026-{count:03d}"

        challenge = Challenge(
            code=code,
            title=title or "Untitled Outcome-Based Challenge",
            department_id=int(dept_id) if dept_id else (departments[0].id if departments else 1),
            sector=sector or "Public Sector Modernization",
            status='published' if is_publish else 'draft',
            
            # Step 1: Problem
            problem_summary=problem_summary or "Problem statement defining operational challenges.",
            problem_details=request.form.get('problem_details'),
            urgency_level=request.form.get('urgency_level', 'High'),

            # Step 2: Current State
            baseline_summary=request.form.get('baseline_summary'),
            current_process=request.form.get('current_process'),
            pain_points=request.form.get('pain_points'),
            affected_users=request.form.get('affected_users'),

            # Step 3: Desired Outcome
            expected_outcome=expected_outcome or "Demonstrable reduction in operational bottleneck.",
            target_improvement=request.form.get('target_improvement'),
            target_kpis_summary=request.form.get('target_kpis_summary'),

            # Step 4: Pilot Scope
            geography=request.form.get('geography'),
            target_users_count=request.form.get('target_users_count'),
            test_facilities=request.form.get('test_facilities'),
            duration_days=int(request.form.get('duration_days', 90)),
            budget_indicative=request.form.get('budget_indicative', '₹10,00,000'),

            # Step 5: Data
            available_datasets=request.form.get('available_datasets'),
            data_sensitivity=request.form.get('data_sensitivity', 'Confidential Government Data'),
            api_availability=request.form.get('api_availability'),
            data_access_terms=request.form.get('data_access_terms'),

            # Step 6: Constraints
            technical_constraints=request.form.get('technical_constraints'),
            security_requirements=request.form.get('security_requirements'),
            integration_requirements=request.form.get('integration_requirements'),

            # Step 7: Evaluation
            evaluation_criteria_notes=request.form.get('evaluation_criteria_notes'),
            success_thresholds=request.form.get('success_thresholds'),

            created_by_user_id=current_user.id,
            published_at=datetime.utcnow() if is_publish else None,
            application_deadline=datetime.utcnow() + timedelta(days=30)
        )
        db.session.add(challenge)
        db.session.commit()

        # Add standard eligibility requirements
        r1 = EligibilityRequirement(challenge_id=challenge.id, criterion_title="Startup Legal Recognition & DPIIT/Registration Certificate", requirement_type="Recognition")
        r2 = EligibilityRequirement(challenge_id=challenge.id, criterion_title="Technical Compatibility with Required Infrastructure", requirement_type="Technical")
        r3 = EligibilityRequirement(challenge_id=challenge.id, criterion_title="Cybersecurity Compliance (ISO 27001 / SOC 2 / CERT-In)", requirement_type="Compliance")
        db.session.add_all([r1, r2, r3])
        db.session.commit()

        action_label = "Published" if is_publish else "Saved Draft for"
        log_audit_event(f"{action_label} Challenge {challenge.code}", "Challenge", challenge.code, challenge.title, current_user)
        flash(f"Challenge {challenge.code} has been successfully {'published' if is_publish else 'saved as draft'}!", "success")
        return redirect(url_for('challenge.view', id=challenge.id))

    return render_template('challenges/builder.html', departments=departments)


@challenge_bp.route('/challenges/ai-assist', methods=['POST'])
@login_required
def ai_assist():
    """AI Assistant endpoint returning structured outcome blueprint from problem text."""
    data = request.get_json() or {}
    prompt = data.get('prompt', '').strip()
    dept = data.get('department', 'Municipal Administration')

    if not prompt:
        return jsonify({'error': 'Problem statement prompt is required.'}), 400

    blueprint = generate_challenge_blueprint(prompt, department_name=dept)
    return jsonify(blueprint)


@challenge_bp.route('/challenges/<int:id>/publish', methods=['POST'])
@login_required
def publish(id):
    challenge = Challenge.query.get_or_404(id)
    if not current_user.is_government and not current_user.is_admin:
        flash("Unauthorized action.", "danger")
        return redirect(url_for('challenge.view', id=id))

    challenge.status = 'published'
    challenge.published_at = datetime.utcnow()
    db.session.commit()
    log_audit_event(f"Published Challenge {challenge.code}", "Challenge", challenge.code, challenge.title, current_user)
    flash(f"Challenge {challenge.code} is now live and published to the startup ecosystem.", "success")
    return redirect(url_for('challenge.view', id=id))


@challenge_bp.route('/challenges/<int:id>/archive', methods=['POST'])
@login_required
def archive(id):
    challenge = Challenge.query.get_or_404(id)
    challenge.status = 'archived'
    db.session.commit()
    log_audit_event(f"Archived Challenge {challenge.code}", "Challenge", challenge.code, challenge.title, current_user)
    flash(f"Challenge {challenge.code} has been archived.", "info")
    return redirect(url_for('challenge.view', id=id))
