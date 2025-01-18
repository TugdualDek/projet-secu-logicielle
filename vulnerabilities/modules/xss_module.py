import requests
from base_module import BaseModule

class Module(BaseModule):
    def run(self, context):
        injection_vectors = context.get('injection_vectors', [])
        module_results = []
        xss_payloads = [
            '<script>alert("XSS")</script>',
            '"><script>alert("XSS")</script>',
            '<img src=x onerror=alert("XSS")>',
            '<svg/onload=alert("XSS")>',
            '<body onload=alert("XSS")>',
        ]
        
        if not injection_vectors:
            context['module_results'] = [{'message': "Aucun vecteur d'injection fourni", 'vulnerable': False}]
            return context
        
        # Flag pour arrêter la recherche dès qu'une vulnérabilité est trouvée
        found_vulnerability = False

        for vector in injection_vectors:
            if found_vulnerability:  # Si une vulnérabilité est déjà trouvée, on arrête les tests
                break

            url = vector.get('url')
            method = vector.get('method', 'get').lower()
            params = vector.get('params', {}) or {}
            data = vector.get('data', {}) or {}
            headers = vector.get('headers', {})

            for payload in xss_payloads:
                test_params = {key: f"{value}{payload}" for key, value in params.items()}
                test_data = {key: f"{value}{payload}" for key, value in data.items()}

                try:
                    if method == 'get':
                        response = requests.get(url, params=test_params, headers=headers, timeout=10)
                    elif method == 'post':
                        response = requests.post(url, data=test_data, headers=headers, timeout=10)
                    else:
                        continue

                    if payload in response.text:
                        result = {
                            'url': url,
                            'method': method.upper(),
                            'payload': payload,
                            'response_length': len(response.text),
                            'response_code': response.status_code,
                            'vulnerable': True
                        }
                        module_results.append(result)
                        found_vulnerability = True  # Marque qu'une vulnérabilité a été trouvée
                        break  # Arrêter de tester les autres payloads pour ce vecteur

                except requests.RequestException as e:
                    module_results.append({'url': url, 'error': str(e), 'vulnerable': False})

        if not module_results:
            module_results.append({'message': "Aucune vulnérabilité XSS détectée", 'vulnerable': False})
        else:
            module_results.append({'vulnerable': True})
    
        context['module_results'] = module_results
        return context