from vulnerabilities.modules.base_module import BaseModule

class Module(BaseModule):
    def run(self, context):
        headers = context.get('response_headers', {})
        # Ajouter les résultats au contexte
        module_results = context.setdefault('module_results', [])
        if not headers:
            # on retourne dans module_results les informations sur l'erreur avec comme clé le nom du module
            module_results.append({
                'Header Analysis': {
                    'error': 'No headers found in the response'
                }
            })

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

        missing_headers = []
        present_headers = []
        for header in security_headers:
            if header not in headers:
                missing_headers.append(header)
            else:
                present_headers.append(header)

        
        if missing_headers:
            module_results.append({
                'Header Analysis': {
                    'missing_headers': missing_headers,
                    'present_headers': present_headers
                }
            })
        return context
