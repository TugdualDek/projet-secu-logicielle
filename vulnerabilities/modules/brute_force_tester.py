import time
import requests
from base_module import BaseModule
import json

class Module(BaseModule):
    def run(self, context):
        url = context.get('url')
        method = context.get('method', 'post')
        content_type = context.get('content_type', 'application/json')
        usernames = context.get('usernames', [])
        passwords = context.get('passwords', [])
        success_status = context.get('success_status', 200)
        max_attempts = context.get('max_attempts', 5)
        delay = context.get('delay', 1)

        module_results = []
        results = {
            'url': url,
            'method': method,
            'tested_credentials': [],
            'vulnerable': False
        }

        attempts = 0

        for username in usernames:
            if attempts >= max_attempts:
                break

            for password in passwords:
                if attempts >= max_attempts:
                    break

                try:
                    # Construire le payload JSON directement
                    payload = {
                        'email': username,
                        'password': password
                    }

                    print(f"Testing credentials - Email: {username}, Password: {password}")

                    # Envoyer la requête
                    response = requests.post(
                        url,
                        json=payload,
                        headers={'Content-Type': content_type},
                        timeout=10
                    )

                    print(f"Response status code: {response.status_code}")

                    # Vérifier si la connexion a réussi
                    auth_successful = response.status_code == success_status

                    results['tested_credentials'].append({
                        'username': username,
                        'password': password,
                        'success': auth_successful,
                        'status_code': response.status_code
                    })

                    if auth_successful:
                        results['vulnerable'] = True
                        break

                    attempts += 1
                    time.sleep(delay)

                except requests.RequestException as e:
                    print(f"Request error: {str(e)}")
                    results.setdefault('errors', []).append(str(e))
                    continue

            if results['vulnerable']:
                break

        if results['vulnerable']:
            module_results.append({
                'message': 'Point d\'entrée vulnérable aux attaques par force brute',
                'vulnerable': True,
                'details': results
            })
        else:
            module_results.append({
                'message': 'Aucune vulnérabilité de force brute détectée',
                'vulnerable': False,
                'details': results
            })

        context['module_results'] = module_results
        return context