#Point d'entrée de l'application Flask.
#Importations
from flask import Flask
from config import Config
from backend.app.routes import init_app
from flask_cors import CORS

app = Flask(__name__)
app.config.from_object(Config)
app.secret_key=Config.SECRET_KEY

CORS(app, supports_credentials=True)

#Initialisation des routes
init_app(app)

if __name__ == '__main__':
    app.run(debug=True)