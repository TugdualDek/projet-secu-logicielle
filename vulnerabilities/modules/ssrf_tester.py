from base_module import BaseModule
import requests

class Module(BaseModule):
    def run(self, context):
        endpoints = context.get('endpoints', context.get('discovered_endpoints', []))
        test_payloads = context.get('test_payloads', [])
        module_results = context.setdefault('module_results', [])
        ssrf_results = []

        # Vérifier que endpoints est une liste de dictionnaires
        if not isinstance(endpoints, list) or not all(isinstance(ep, dict) for ep in endpoints):
            module_results.append({
                'SSRF Test': {
                    'error': 'Les endpoints fournis ne sont pas valides. Attendu une liste de dictionnaires.'
                }
            })
            return context

        if not endpoints:
            return context

        for endpoint in endpoints:
            url = endpoint['url']
            method = endpoint.get('method', 'get').lower()
            param_name = endpoint.get('param_name')
            params = endpoint.get('params', {})
            original_params = params.copy()

            for payload in test_payloads:
                if param_name:
                    params[param_name] = payload
                else:
                    # Si aucun paramètre spécifique, on saute ce endpoint
                    continue

                try:
                    if method == 'get':
                        response = requests.get(url, params=params, timeout=10)
                    elif method == 'post':
                        response = requests.post(url, data=params, timeout=10)
                    else:
                        continue

                    # Analyser la réponse pour détecter une éventuelle vulnérabilité
                    if self.is_ssrf_vulnerable(response, payload):
                        ssrf_results.append({
                            'url': url,
                            'method': method,
                            'payload': payload,
                            'params': params.copy(),
                            'vulnerable': True
                        })
                    else:
                        ssrf_results.append({
                            'url': url,
                            'method': method,
                            'payload': payload,
                            'params': params.copy(),
                            'vulnerable': False
                        })

                except requests.RequestException as e:
                    ssrf_results.append({
                        'url': url,
                        'method': method,
                        'payload': payload,
                        'params': params.copy(),
                        'error': f"Erreur lors de la requête : {e}"
                    })

                # Réinitialiser les paramètres pour le prochain test
                params = original_params.copy()

        module_results.append({
            'SSRF Test': ssrf_results
        })

        return context

    def is_ssrf_vulnerable(self, response, payload):
        """
        Fonction pour déterminer si la réponse indique une vulnérabilité SSRF.
        Cette fonction doit être adaptée en fonction de l'application cible
        et des signatures de réponse attendues.
        """
        return payload in response.text
    