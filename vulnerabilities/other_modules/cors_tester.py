from vulnerabilities.modules.base_module import BaseModule
import requests

class Module(BaseModule):
    def run(self, context):
        url = context.get('url', context.get('target'))
        test_origins = context.get('test_origins', ['http://evil.com', 'null'])
        module_results = context.setdefault('module_results', [])
        cors_results = []

        for origin in test_origins:
            headers = {'Origin': origin}
            try:
                response = requests.get(url, headers=headers)
                acao = response.headers.get('Access-Control-Allow-Origin')
                misconfig = acao == '*' or acao == origin
                cors_results.append({
                    'origin': origin,
                    'misconfiguration': misconfig,
                    'acao': acao
                })
            except requests.RequestException as e:
                cors_results.append({
                    'origin': origin,
                    'error': str(e)
                })

        # Ajouter les résultats au contexte
        module_results.append({
            'CORS Analysis': cors_results
        })
        return context