import os
from flask import Flask, send_from_directory
from backend.main import create_api  # Importer la fonction qui crée l'API
from backend.config.settings import API_CONFIG
from backend.kernel.kernel import Kernel

app = Flask(__name__, static_folder='frontend/build')

app.kernel = Kernel()  # Crée une instance du Kernel

api_app = create_api(app)  # Crée l'application API sans lancer un serveur séparé

# Enregistre le blueprint directement dans l'application principale
app.register_blueprint(api_app.blueprints['api'], url_prefix='/api')

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    # Sert les fichiers statiques du frontend
    if path and os.path.exists(app.static_folder + '/' + path):
        return send_from_directory(app.static_folder, path)
    return send_from_directory(app.static_folder, 'index.html')

if __name__ == '__main__':
    # Lancement du serveur unique pour les routes API et le frontend
    app.run(host=API_CONFIG['HOST'], port=API_CONFIG['PORT'], debug=API_CONFIG['DEBUG'])
