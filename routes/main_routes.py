from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash
from flask_login import current_user, login_required
from models import db, Challenge, Startup, Pilot, Department, Notification
from services.seed_data import seed_database
from services.audit_service import log_audit_event

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def landing():
    active_challenges_count = Challenge.query.filter_by(status='published').count()
    active_pilots_count = Pilot.query.count()
    startups_count = Startup.query.count()
    return render_template(
        'landing.html',
        active_challenges_count=active_challenges_count or 18,
        active_pilots_count=active_pilots_count or 12,
        startups_count=startups_count or 247
    )

@main_bp.route('/demo-tour')
def demo_tour():
    """Interactive step-by-step guided story of GovPilot from Problem to Pilot to Scale."""
    pilot = Pilot.query.filter_by(code="GP-MH-2026-00421").first()
    challenge = Challenge.query.filter_by(code="CH-TRANS-2026-001").first()
    return render_template('demo/tour.html', pilot=pilot, challenge=challenge)

@main_bp.route('/search')
def global_search():
    query = request.args.get('q', '').strip()
    if not query:
        return render_template('search_results.html', query=query, challenges=[], startups=[], pilots=[], departments=[])

    search_term = f"%{query}%"
    challenges = Challenge.query.filter(
        (Challenge.title.ilike(search_term)) | 
        (Challenge.code.ilike(search_term)) | 
        (Challenge.sector.ilike(search_term)) |
        (Challenge.problem_summary.ilike(search_term))
    ).all()

    startups = Startup.query.filter(
        (Startup.name.ilike(search_term)) | 
        (Startup.sector.ilike(search_term)) | 
        (Startup.core_technology.ilike(search_term)) |
        (Startup.summary.ilike(search_term))
    ).all()

    pilots = Pilot.query.filter(
        (Pilot.title.ilike(search_term)) | 
        (Pilot.code.ilike(search_term)) |
        (Pilot.status.ilike(search_term))
    ).all()

    departments = Department.query.filter(
        (Department.name.ilike(search_term)) | 
        (Department.code.ilike(search_term)) | 
        (Department.sector.ilike(search_term))
    ).all()

    return render_template(
        'search_results.html',
        query=query,
        challenges=challenges,
        startups=startups,
        pilots=pilots,
        departments=departments
    )

@main_bp.route('/knowledge-library')
def knowledge_library():
    """Searchable innovation library of completed and validated pilots."""
    query = request.args.get('q', '').strip()
    sector = request.args.get('sector', '')

    pilots_query = Pilot.query
    if query:
        search_term = f"%{query}%"
        pilots_query = pilots_query.filter(
            (Pilot.title.ilike(search_term)) | 
            (Pilot.objectives_summary.ilike(search_term)) |
            (Pilot.code.ilike(search_term))
        )
    if sector:
        pilots_query = pilots_query.join(Department).filter(Department.sector == sector)

    pilots = pilots_query.all()
    sectors = [d[0] for d in db.session.query(Department.sector).distinct() if d[0]]

    return render_template('knowledge/library.html', pilots=pilots, query=query, selected_sector=sector, sectors=sectors)

@main_bp.route('/notifications/read-all', methods=['POST'])
@login_required
def mark_all_notifications_read():
    Notification.query.filter(
        (Notification.user_id == current_user.id) | 
        (Notification.target_role == current_user.role)
    ).update({'is_read': True})
    db.session.commit()
    return jsonify({'success': True})

@main_bp.route('/reset-demo-data', methods=['POST', 'GET'])
def reset_demo():
    """Drops tables and re-seeds fresh demo data."""
    try:
        db.drop_all()
        seed_database()
        flash("Demo data has been successfully reset to initial state!", "success")
    except Exception as e:
        flash(f"Error resetting database: {e}", "danger")
    return redirect(url_for('main.landing'))
