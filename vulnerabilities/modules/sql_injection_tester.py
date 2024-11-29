import requests
import re

class Module:
    def run(self, context):
        injection_vectors = context.get('injection_vectors', [])
        module_results = []

        # Chargement des signatures d'erreur
        error_signatures = [
            'you have an error in your sql syntax',
            'warning: mysql',
            'unclosed quotation mark after the character string',
            'quoted string not properly terminated',
            'invalid query',
            'sql syntax',
            'odbc drivers error',
            'Warning: mysql'
        ]

        # Regroupement des payloads par URL
        url_payloads = {}
        for vector in injection_vectors:
            url = vector['url']
            url_payloads.setdefault(url, []).append(vector)

        vulnerable_urls = set()

        for url, vectors in url_payloads.items():
            if url in vulnerable_urls:
                continue  # URL déjà vulnérable

            for vector in vectors:
                method = vector.get('method', 'get')
                params = vector.get('params')
                data = vector.get('data')
                payload = params or data  # Le payload injecté

                print(f"Testing {method.upper()} {url} with payload {payload}")

                try:
                    # Envoi de la requête avec le payload
                    if method == 'get':
                        response = requests.get(url, params=params, timeout=10)
                    elif method == 'post':
                        response = requests.post(url, data=data, timeout=10)
                    else:
                        continue  # Méthode non supportée

                    # Analyse de la réponse pour détecter des signatures d'erreur
                    for signature in error_signatures:
                        if re.search(signature, response.text, re.IGNORECASE):
                            # Vulnérabilité potentielle détectée
                            result = {
                                'type': 'query_parameter' if method.lower() == 'get' else 'form',
                                'url': url,
                                'method': method.upper(),
                                'payload': payload,
                                'error_signature': signature
                            }
                            module_results.append(result)
                            vulnerable_urls.add(url)
                            break  # On arrête après la première signature correspondante

                    # Si une vulnérabilité a été trouvée, on n'a pas besoin de tester plus de payloads
                    if url in vulnerable_urls:
                        break

                except requests.RequestException as e:
                    # En cas d'erreur de requête, ajouter l'erreur aux résultats
                    error_result = {
                        'url': url,
                        'method': method.upper(),
                        'payload': payload,
                        'error': str(e)
                    }
                    module_results.append(error_result)
                    # Vous pouvez décider d'arrêter les tests sur cette URL en cas d'erreur critique

        # Stocker les résultats dans le contexte
        context['module_results'] = module_results
        return context
