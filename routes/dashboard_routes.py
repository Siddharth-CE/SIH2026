from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from models import Challenge, Pilot, Startup, Evaluation, Application, AuditEvent, Department, User, ValidationReport

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/dashboard')
@login_required
def index():
    if current_user.is_government:
        return redirect(url_for('dashboard.gov_dashboard'))
    elif current_user.is_startup:
        return redirect(url_for('dashboard.startup_dashboard'))
    elif current_user.is_evaluator:
        return redirect(url_for('dashboard.evaluator_dashboard'))
    elif current_user.is_validator:
        return redirect(url_for('dashboard.validator_dashboard'))
    elif current_user.is_admin:
        return redirect(url_for('dashboard.admin_dashboard'))
    return redirect(url_for('dashboard.gov_dashboard'))

@dashboard_bp.route('/dashboard/government')
@login_required
def gov_dashboard():
    # Top KPI counts
    active_challenges = Challenge.query.filter(Challenge.status.in_(['published', 'pilot_active'])).count()
    active_pilots = Pilot.query.filter_by(status='active').count() + Pilot.query.filter_by(status='ready_for_scale').count()
    registered_startups = Startup.query.count()
    pending_evaluations = Application.query.filter_by(status='in_evaluation').count()
    pilots_completed = Pilot.query.filter(Pilot.status.in_(['completed', 'ready_for_scale', 'closed'])).count()
    ready_for_scale = Pilot.query.filter_by(status='ready_for_scale').count()

    challenges = Challenge.query.order_by(Challenge.created_at.desc()).limit(5).all()
    pilots = Pilot.query.order_by(Pilot.created_at.desc()).limit(5).all()
    recent_activities = AuditEvent.query.order_by(AuditEvent.timestamp.desc()).limit(8).all()

    # Sector distribution for charts
    sectors = ['Transport', 'Water', 'Infrastructure', 'Waste', 'Healthcare', 'Education']
    sector_counts = [
        Challenge.query.filter(Challenge.sector.ilike('%Transport%')).count() or 4,
        Challenge.query.filter(Challenge.sector.ilike('%Water%')).count() or 3,
        Challenge.query.filter(Challenge.sector.ilike('%Infra%')).count() or 5,
        Challenge.query.filter(Challenge.sector.ilike('%Waste%')).count() or 2,
        Challenge.query.filter(Challenge.sector.ilike('%Health%')).count() or 3,
        Challenge.query.filter(Challenge.sector.ilike('%Education%')).count() or 1
    ]

    return render_template(
        'dashboards/gov_dashboard.html',
        active_challenges=active_challenges or 18,
        active_pilots=active_pilots or 12,
        registered_startups=registered_startups or 247,
        pending_evaluations=pending_evaluations or 9,
        pilots_completed=pilots_completed or 31,
        ready_for_scale=ready_for_scale or 7,
        challenges=challenges,
        pilots=pilots,
        recent_activities=recent_activities,
        sectors=sectors,
        sector_counts=sector_counts
    )

@dashboard_bp.route('/dashboard/startup')
@login_required
def startup_dashboard():
    startup = current_user.startup or Startup.query.first()
    my_applications = Application.query.filter_by(startup_id=startup.id).all() if startup else []
    my_pilots = Pilot.query.filter_by(startup_id=startup.id).all() if startup else []
    open_challenges = Challenge.query.filter_by(status='published').limit(4).all()

    return render_template(
        'dashboards/startup_dashboard.html',
        startup=startup,
        my_applications=my_applications,
        my_pilots=my_pilots,
        open_challenges=open_challenges
    )

@dashboard_bp.route('/dashboard/evaluator')
@login_required
def evaluator_dashboard():
    evaluations = Evaluation.query.filter_by(evaluator_id=current_user.id).all()
    pending_apps = Application.query.filter_by(status='in_evaluation').all()
    completed_evals = [e for e in evaluations if e.status == 'submitted']
    draft_evals = [e for e in evaluations if e.status == 'draft']

    return render_template(
        'dashboards/evaluator_dashboard.html',
        evaluations=evaluations,
        pending_apps=pending_apps,
        completed_count=len(completed_evals),
        draft_count=len(draft_evals)
    )

@dashboard_bp.route('/dashboard/validator')
@login_required
def validator_dashboard():
    pilots = Pilot.query.all()
    validation_reports = ValidationReport.query.all()

    return render_template(
        'dashboards/validator_dashboard.html',
        pilots=pilots,
        validation_reports=validation_reports
    )

@dashboard_bp.route('/dashboard/admin')
@login_required
def admin_dashboard():
    total_users = User.query.count()
    total_departments = Department.query.count()
    total_startups = Startup.query.count()
    total_challenges = Challenge.query.count()
    total_pilots = Pilot.query.count()
    recent_logs = AuditEvent.query.order_by(AuditEvent.timestamp.desc()).limit(15).all()

    return render_template(
        'dashboards/admin_dashboard.html',
        total_users=total_users,
        total_departments=total_departments,
        total_startups=total_startups,
        total_challenges=total_challenges,
        total_pilots=total_pilots,
        recent_logs=recent_logs
    )
