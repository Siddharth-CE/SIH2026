from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models import db, Startup, StartupDeployment, StartupCertification
from services.audit_service import log_audit_event

startup_bp = Blueprint('startup', __name__)

@startup_bp.route('/startups')
def index():
    query = request.args.get('q', '').strip()
    sector = request.args.get('sector', '')
    trl = request.args.get('trl', '')

    q = Startup.query
    if query:
        search_term = f"%{query}%"
        q = q.filter(
            (Startup.name.ilike(search_term)) | 
            (Startup.core_technology.ilike(search_term)) | 
            (Startup.capabilities.ilike(search_term)) |
            (Startup.summary.ilike(search_term))
        )
    if sector:
        q = q.filter(Startup.sector.ilike(f"%{sector}%"))
    if trl:
        q = q.filter(Startup.trl_level.ilike(f"%{trl}%"))

    startups = q.all()
    sectors = [s[0] for s in db.session.query(Startup.sector).distinct() if s[0]]

    return render_template(
        'startups/index.html',
        startups=startups,
        sectors=sectors,
        search_query=query,
        selected_sector=sector,
        selected_trl=trl
    )


@startup_bp.route('/startups/<int:id>')
def passport(id):
    startup = Startup.query.get_or_404(id)
    return render_template('startups/passport.html', startup=startup)


@startup_bp.route('/startups/passport/edit', methods=['GET', 'POST'])
@login_required
def edit_passport():
    startup = current_user.startup
    if not startup and not current_user.is_admin:
        flash("Only registered startup representatives can edit this Innovation Passport.", "danger")
        return redirect(url_for('startup.index'))

    if not startup and current_user.is_admin:
        startup = Startup.query.first()

    if request.method == 'POST':
        startup.name = request.form.get('name', startup.name)
        startup.legal_name = request.form.get('legal_name', startup.legal_name)
        startup.registration_number = request.form.get('registration_number', startup.registration_number)
        startup.startup_recognition_number = request.form.get('startup_recognition_number', startup.startup_recognition_number)
        startup.founded_year = int(request.form.get('founded_year', startup.founded_year or 2023))
        startup.headquarters = request.form.get('headquarters', startup.headquarters)
        startup.website = request.form.get('website', startup.website)
        startup.founders = request.form.get('founders', startup.founders)
        startup.employee_count = request.form.get('employee_count', startup.employee_count)
        startup.summary = request.form.get('summary', startup.summary)
        startup.sector = request.form.get('sector', startup.sector)
        startup.core_technology = request.form.get('core_technology', startup.core_technology)
        startup.product_name = request.form.get('product_name', startup.product_name)
        startup.product_description = request.form.get('product_description', startup.product_description)
        startup.architecture_overview = request.form.get('architecture_overview', startup.architecture_overview)
        startup.deployment_model = request.form.get('deployment_model', startup.deployment_model)
        startup.trl_level = request.form.get('trl_level', startup.trl_level)
        startup.capabilities = request.form.get('capabilities', startup.capabilities)
        startup.ip_details = request.form.get('ip_details', startup.ip_details)
        startup.cybersecurity_standard = request.form.get('cybersecurity_standard', startup.cybersecurity_standard)
        
        db.session.commit()
        log_audit_event("Updated Innovation Passport", "Startup", str(startup.id), startup.name, current_user)
        flash("Your Startup Innovation Passport has been updated successfully!", "success")
        return redirect(url_for('startup.passport', id=startup.id))

    return render_template('startups/edit_passport.html', startup=startup)
