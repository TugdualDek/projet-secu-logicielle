from flask import Flask
from .config.settings import DATABASE_CONFIG, API_CONFIG
from .database.init_db import init_database

def create_app():
    app = Flask(__name__)

    init_database()

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host=API_CONFIG['HOST'], port=API_CONFIG['PORT'], debug=API_CONFIG['DEBUG'])
