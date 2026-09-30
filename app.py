import os
from flask import Flask, render_template, send_from_directory
from config import Config
from models import db, login_manager
from routes import (
    auth_bp, main_bp, dashboard_bp, challenge_bp, startup_bp,
    application_bp, evaluation_bp, pilot_bp, validation_bp, scale_bp,
    admin_bp, api_bp
)
from services.seed_data import seed_database

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)

    # Ensure instance and upload directories exist (safely ignoring read-only root in serverless)
    try:
        os.makedirs(os.path.join(app.root_path, 'instance'), exist_ok=True)
    except OSError:
        pass

    try:
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    except OSError:
        pass

    # Register Blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(challenge_bp)
    app.register_blueprint(startup_bp)
    app.register_blueprint(application_bp)
    app.register_blueprint(evaluation_bp)
    app.register_blueprint(pilot_bp)
    app.register_blueprint(validation_bp)
    app.register_blueprint(scale_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(api_bp)

    # File uploads serving endpoint
    @app.route('/uploads/<path:filename>')
    def uploaded_file(filename):
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

    # Error handlers
    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('base.html'), 404

    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return render_template('base.html'), 500

    # Auto-initialize and seed database safely
    with app.app_context():
        try:
            seed_database()
        except Exception as e:
            print(f"[GovPilot Warning] Auto-seeding encountered notice: {e}")

    return app

app = create_app()

if __name__ == '__main__':
    print("=" * 70)
    print("GovPilot - Innovation Procurement & Pilot Management Platform")
    print("Running locally at: http://127.0.0.1:5000")
    print("Demo Users:")
    print("  • Government Officer: government@govpilot.demo / Password123")
    print("  • Startup Founder:    startup@innovate.demo    / Password123")
    print("  • Expert Evaluator:   expert@review.demo       / Password123")
    print("  • Validator Auditor:  validator@audit.demo     / Password123")
    print("  • Admin:              admin@govpilot.demo      / Password123")
    print("=" * 70)
    app.run(host='127.0.0.1', port=5000, debug=True)
