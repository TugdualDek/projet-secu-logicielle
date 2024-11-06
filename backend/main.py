from flask import Flask
from .config.settings import DATABASE_CONFIG, API_CONFIG
from .database.init_db import init_database
from .api.server import api  # Importation du blueprint api

def create_api():
    app = Flask(__name__)

    # Initialize database
    # init_database()

    # Register the API blueprint
    app.register_blueprint(api, url_prefix='/api')
    
    return app