from flask import Flask
from .config.settings import DATABASE_CONFIG, API_CONFIG
from .database.init_db import init_database
from .api.server import api  # Importation du blueprint api

def create_api():
    app = Flask(__name__)

    # Initialize the database only if there has never been a connection
    if not app.config.get('database_initialized'):
        init_database()
        # Set the flag to avoid initializing the database multiple times but do it permanently
        app.config['database_initialized'] = True

    # Register the API blueprint
    app.register_blueprint(api, url_prefix='/api')
    
    return app