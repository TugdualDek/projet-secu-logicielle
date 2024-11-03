# Indique que le dossier routes est un package Python.
# Importations
from flask import blueprints
from ..routes.auth_routes import auth_bp

def init_app(app):
    app.register_blueprint(auth_bp)