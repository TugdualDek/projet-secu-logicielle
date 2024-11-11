from base_module import BaseModule
import requests

class Module(BaseModule):
    def run(self, context):
        url = context.get('url')
        test_origins = context.get('test_origins', ['http://evil.com', 'null'])
        results = []

        for origin in test_origins:
            headers = {'Origin': origin}
            try:
                response = requests.get(url, headers=headers)
                acao = response.headers.get('Access-Control-Allow-Origin')
                misconfig = acao == '*' or acao == origin
                results.append({
                    'origin': origin,
                    'misconfiguration': misconfig,
                    'acao': acao
                })
            except requests.RequestException as e:
                results.append({
                    'origin': origin,
                    'error': str(e)
                })

        context.setdefault('results', {})['cors_analysis'] = results
        return context