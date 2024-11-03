# Indique que le dossier routes est un package Python.
# backend/app/routes/__init__.py
from flask import Blueprint
from .auth_routes import auth_bp
from .scan_routes import scan_bp

def init_app(app):
    # Utilisation du préfixe /auth pour les routes d'authentification
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(scan_bp, url_prefix='/scan')