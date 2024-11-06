import os
from flask import Flask, send_from_directory
from backend.main import create_api  # Importer la fonction qui crée l'API

app = Flask(__name__, static_folder='frontend/build')
api_app = create_api()  # Crée l'application API sans lancer un serveur séparé

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
    app.run(host='0.0.0.0', port=5000, debug=True)
