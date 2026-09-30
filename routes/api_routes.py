from flask import Blueprint, jsonify, request
from flask_login import current_user
from models import db, Challenge, Startup, Application, Evaluation, Pilot, PilotKPI, Notification, AuditEvent

api_bp = Blueprint('api', __name__, url_prefix='/api')

@api_bp.route('/challenges')
def get_challenges():
    challenges = Challenge.query.all()
    return jsonify([{
        'id': c.id,
        'code': c.code,
        'title': c.title,
        'sector': c.sector,
        'status': c.status,
        'department': c.department.name if c.department else None,
        'duration_days': c.duration_days,
        'applications_count': len(c.applications)
    } for c in challenges])


@api_bp.route('/startups')
def get_startups():
    startups = Startup.query.all()
    return jsonify([{
        'id': s.id,
        'name': s.name,
        'sector': s.sector,
        'core_technology': s.core_technology,
        'trl_level': s.trl_level,
        'deployments_count': len(s.deployments),
        'cybersecurity_certified': s.cybersecurity_certified
    } for s in startups])


@api_bp.route('/pilots/<int:id>/kpis')
def get_pilot_kpis(id):
    pilot = Pilot.query.get_or_404(id)
    kpi_list = []
    for k in pilot.kpis:
        obs_data = [{
            'date': obs.observation_date.strftime('%Y-%m-%d'),
            'period': obs.period_label,
            'value': obs.recorded_value,
            'verified': obs.verified_by_validator
        } for obs in k.observations]

        kpi_list.append({
            'id': k.id,
            'name': k.name,
            'unit': k.unit,
            'baseline': k.baseline_value,
            'target': k.target_value,
            'current': k.current_value,
            'status': k.status,
            'higher_is_better': k.higher_is_better,
            'observations': obs_data
        })

    return jsonify({
        'pilot_code': pilot.code,
        'pilot_title': pilot.title,
        'kpis': kpi_list
    })


@api_bp.route('/notifications')
def get_notifications():
    if not current_user.is_authenticated:
        return jsonify([])

    notifs = Notification.query.filter(
        (Notification.user_id == current_user.id) | 
        (Notification.target_role == current_user.role)
    ).order_by(Notification.created_at.desc()).limit(10).all()

    return jsonify([{
        'id': n.id,
        'title': n.title,
        'message': n.message,
        'category': n.category,
        'link_url': n.link_url,
        'is_read': n.is_read,
        'created_at': n.created_at.strftime('%d %b %H:%M')
    } for n in notifs])
