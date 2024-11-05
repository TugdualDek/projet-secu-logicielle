import subprocess
import os
from flask import Flask, send_from_directory
from backend.main import create_app

app = Flask(__name__, static_folder='frontend/build')
api = create_app() 

""" @app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path and os.path.exists(app.static_folder + '/' + path):
        return send_from_directory(app.static_folder, path)
    return send_from_directory(app.static_folder, 'index.html') """

# Toutes les routes /api sont redirigées vers le backend
@app.route('/api/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def api_proxy(path):
    return api.handle_request()

def start_development_server():
    # Démarrage du serveur de développement React
    return False
"""    frontend_process = subprocess.Popen(
        'npm start',
        shell=True,
        cwd='./frontend'
    )

    try:
        # Démarrage du serveur Flask
        app.run(port=5000, debug=True)
    finally:
        frontend_process.terminate() """

if __name__ == '__main__':
    if os.environ.get('FLASK_ENV') == 'development':
        start_development_server()
    else:
        # Mode production
        app.run(host='0.0.0.0', port=5000)