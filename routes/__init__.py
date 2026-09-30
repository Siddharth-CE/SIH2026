from routes.auth_routes import auth_bp
from routes.main_routes import main_bp
from routes.dashboard_routes import dashboard_bp
from routes.challenge_routes import challenge_bp
from routes.startup_routes import startup_bp
from routes.application_routes import application_bp
from routes.evaluation_routes import evaluation_bp
from routes.pilot_routes import pilot_bp
from routes.validation_routes import validation_bp
from routes.scale_routes import scale_bp
from routes.admin_routes import admin_bp
from routes.api_routes import api_bp

__all__ = [
    'auth_bp',
    'main_bp',
    'dashboard_bp',
    'challenge_bp',
    'startup_bp',
    'application_bp',
    'evaluation_bp',
    'pilot_bp',
    'validation_bp',
    'scale_bp',
    'admin_bp',
    'api_bp'
]
