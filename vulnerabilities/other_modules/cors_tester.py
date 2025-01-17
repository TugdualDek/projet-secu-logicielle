from vulnerabilities.modules.base_module import BaseModule
import requests
from urllib.parse import urlparse
import socket

class Module(BaseModule):
    def run(self, context):
        url = context.get('url', context.get('target'))
        test_origins = context.get('test_origins', ['http://localhost:3000', 'http://evil.com', 'null'])
        module_results = context.setdefault('module_results', [])
        cors_results = []

        # Vérifier si l'URL est valide
        try:
            parsed_url = urlparse(url)
            # Vérifier si le serveur est accessible
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2)  # Timeout de 2 secondes
            result = sock.connect_ex((parsed_url.hostname or '', parsed_url.port or 80))
            sock.close()

            if result != 0:
                raise ConnectionError(f"Le serveur {url} n'est pas accessible")

        except Exception as e:
            module_results.append({
                'CORS Analysis': [{
                    'error': f"URL invalide ou serveur inaccessible: {str(e)}"
                }]
            })
            return context

        # Test CORS avec gestion d'erreurs améliorée
        for origin in test_origins:
            headers = {'Origin': origin}
            try:
                response = requests.get(
                    url, 
                    headers=headers, 
                    timeout=5,  # Timeout de 5 secondes
                    verify=False  # Désactiver la vérification SSL pour les tests
                )
                acao = response.headers.get('Access-Control-Allow-Origin')
                acam = response.headers.get('Access-Control-Allow-Methods')
                acah = response.headers.get('Access-Control-Allow-Headers')
                
                cors_results.append({
                    'origin': origin,
                    'status_code': response.status_code,
                    'headers': {
                        'Access-Control-Allow-Origin': acao,
                        'Access-Control-Allow-Methods': acam,
                        'Access-Control-Allow-Headers': acah
                    },
                    'misconfiguration': acao == '*' or acao == origin
                })
            except requests.Timeout:
                cors_results.append({
                    'origin': origin,
                    'error': 'Timeout de la requête'
                })
            except requests.ConnectionError as e:
                cors_results.append({
                    'origin': origin,
                    'error': f"Erreur de connexion: {str(e)}"
                })
            except Exception as e:
                cors_results.append({
                    'origin': origin,
                    'error': f"Erreur inattendue: {str(e)}"
                })

        module_results.append({
            'CORS Analysis': cors_results
        })
        return context
