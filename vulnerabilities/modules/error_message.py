from base_module import BaseModule
import requests
import re

class Module(BaseModule):
    def run(self, context):
        """
        Analyse les messages d'erreur potentiellement sensibles
        """
        url = context.get('url', context.get('target'))
        module_results = context.setdefault('module_results', [])
        error_results = []

        if not url:
            module_results.append({
                'Error Message Analysis': {
                    'error': 'Aucune URL fournie'
                }
            })
            return context

        sensitive_patterns = [
            r'database error',
            r'SQL syntax',
            r'stack trace',
            r'internal server error',
            r'debug information'
        ]

        try:
            response = requests.get(url)
            detected_patterns = []

            for pattern in sensitive_patterns:
                if re.search(pattern, response.text, re.IGNORECASE):
                    detected_patterns.append({
                        'pattern': pattern,
                        'detected': True,
                        'severity': 'high'
                    })

            error_results = {
                'url': url,
                'status_code': response.status_code,
                'patterns_detected': detected_patterns if detected_patterns else 'No sensitive patterns detected',
                'vulnerable': len(detected_patterns) > 0
            }

        except requests.exceptions.RequestException as e:
            error_results = {
                'url': url,
                'error': str(e),
                'status': 'failed'
            }

        module_results.append({
            'Error Message Analysis': error_results
        })
        return context
