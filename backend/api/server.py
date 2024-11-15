from flask import Blueprint
from backend.api.routes.scan_routes import scans_bp
from .routes.report_routes import reports_bp

api = Blueprint('api', __name__)

# Register route blueprints
api.register_blueprint(scans_bp, url_prefix='/scans')
api.register_blueprint(reports_bp, url_prefix='/reports')

