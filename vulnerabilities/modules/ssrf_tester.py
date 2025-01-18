from vulnerabilities.modules.base_module import BaseModule
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

        # Ensemble pour suivre les endpoints vulnérables
        vulnerable_endpoints = set()

        # Regrouper les endpoints par URL
        url_endpoints = {}
        for endpoint in endpoints:
            url = endpoint['url']
            url_endpoints.setdefault(url, []).append(endpoint)

        for url, endpoint_list in url_endpoints.items():
            # Si l'URL est déjà marquée comme vulnérable, passer au suivant
            if url in vulnerable_endpoints:
                continue

            for endpoint in endpoint_list:
                method = endpoint.get('method', 'get').lower()
                param_name = endpoint.get('param_name')
                params = endpoint.get('params', {})
                original_params = params.copy()

                is_vulnerable = False  # Indicateur de vulnérabilité pour cet endpoint

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
                            vulnerable_endpoints.add(url)
                            is_vulnerable = True
                            break  # Arrêter les tests de payloads pour ce endpoint
                        else:
                            continue  # Passer au prochain payload

                    except requests.RequestException as e:
                        continue  # Ignorer les erreurs de requête

                    # Réinitialiser les paramètres pour le prochain test
                    params = original_params.copy()

                if is_vulnerable:
                    break  # Arrêter de tester d'autres endpoints pour cette URL


        if len(module_results) >= 1:
            module_results.append(
                ssrf_results,
                {
                'vulnerable': True
            })
        else:
            module_results.append({
                'message': 'No SSRF vulnerabilities detected',
                'vulnerable': False
            })

        return context

    def is_ssrf_vulnerable(self, response, payload):
        """
        Fonction pour déterminer si la réponse indique une vulnérabilité SSRF.
        Cette fonction doit être adaptée en fonction de l'application cible
        et des signatures de réponse attendues.
        """
        return payload in response.text
