from flask import Flask
from backend.config.settings import DATABASE_CONFIG, API_CONFIG
from backend.database.init_db import init_database
from backend.api.server import api

def create_api(app=None):
    """
    create_api Crée l'application API Flask
    :param app: Instance de l'application Flask
    :return: Instance de l'application Flask
    """
    if app is None:
        app = Flask(__name__)

    # Initialiser la base de données si elle ne l'a pas été
    if not app.config.get('database_initialized'):
        init_database()
        app.config['database_initialized'] = True

    # Enregistrer le blueprint de l'API
    app.register_blueprint(api, url_prefix='/api')
    
    return app