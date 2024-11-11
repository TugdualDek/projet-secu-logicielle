from base_module import BaseModule

class Module(BaseModule):
    def run(self, context):
        headers = context.get('response_headers')
        if not headers:
            context.setdefault('errors', []).append("Aucune en-tête trouvée pour l'analyse des en-têtes.")
            return context

        security_headers = [
            'Strict-Transport-Security',
            'Content-Security-Policy',
            'X-Content-Type-Options',
            'X-Frame-Options',
            'X-XSS-Protection',
            'Referrer-Policy',
            'Permissions-Policy'
        ]

        results = {}
        for header in security_headers:
            value = headers.get(header)
            results[header] = {
                'present': value is not None,
                'value': value
            }

        # Stocker les résultats finaux dans context['results']
        context.setdefault('results', {})['security_headers_analysis'] = results
        return context