from flask import Flask
from .config.settings import DATABASE_CONFIG, API_CONFIG
from .database.init_db import init_database
from .api.server import api  # Importation du blueprint api

def create_api(app=None):
    if app is None:
        app = Flask(__name__)

    # Initialiser la base de données si elle ne l'a pas été
    if not app.config.get('database_initialized'):
        init_database()
        app.config['database_initialized'] = True

    # Enregistrer le blueprint de l'API
    app.register_blueprint(api, url_prefix='/api')
    
    return app