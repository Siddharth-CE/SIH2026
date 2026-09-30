from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from flask_login import login_user, logout_user, login_required, current_user
from models import db, User
from services.audit_service import log_audit_event
from datetime import datetime

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))

    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()
        remember = bool(request.form.get('remember'))

        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            login_user(user, remember=remember)
            user.last_login = datetime.utcnow()
            db.session.commit()
            log_audit_event("User Logged In", "User", str(user.id), f"Logged in as {user.role}", user)
            flash(f"Welcome back, {user.name} ({user.role.title()})", "success")
            
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            return redirect(url_for('dashboard.index'))
        else:
            flash("Invalid email or password. Please try the demo accounts.", "danger")

    return render_template('login.html')


@auth_bp.route('/quick-login/<role>')
def quick_login(role):
    """One-click login switcher for demo purposes."""
    role_email_map = {
        'government': 'government@govpilot.demo',
        'startup': 'startup@innovate.demo',
        'evaluator': 'expert@review.demo',
        'validator': 'validator@audit.demo',
        'admin': 'admin@govpilot.demo'
    }
    email = role_email_map.get(role.lower())
    if email:
        user = User.query.filter_by(email=email).first()
        if user:
            login_user(user)
            user.last_login = datetime.utcnow()
            db.session.commit()
            log_audit_event("Quick Demo Switcher Login", "User", str(user.id), f"Switched to {user.role}", user)
            flash(f"Logged in as {user.name} ({user.role.title()} Demo)", "info")
            return redirect(url_for('dashboard.index'))
    
    flash("Demo account not found.", "warning")
    return redirect(url_for('auth.login'))


@auth_bp.route('/logout')
@login_required
def logout():
    log_audit_event("User Logged Out", "User", str(current_user.id), "User signed out", current_user)
    logout_user()
    flash("You have been signed out safely.", "info")
    return redirect(url_for('main.landing'))
