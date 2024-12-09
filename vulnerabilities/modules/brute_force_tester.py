from base_module import BaseModule
import requests
import time
import logging

class Module(BaseModule):
    def run(self, context):
        url = context.get('url')
        method = context.get('method', 'post').lower()
        content_type = context.get('content_type', 'application/json')
        usernames = context.get('usernames', [])
        passwords = context.get('passwords', [])
        max_attempts = context.get('max_attempts', 20)
        delay = context.get('delay', 1)
        username_field = context.get('username_field', 'email')
        password_field = context.get('password_field', 'password')

        module_results = []
        results = {
            'url': url,
            'method': method.upper(),
            'tested_credentials': [],
            'successful_attempts': 0,
            'failed_attempts': 0,
            'errors': [],
            'vulnerable': False
        }

        # Obtenir le token CSRF initial si nécessaire
        session = requests.Session()
        try:
            initial_response = session.get(url)
            csrf_token = self._extract_csrf_token(initial_response.text)
        except Exception as e:
            logging.error(f"Erreur lors de la récupération du token CSRF: {e}")
            csrf_token = None

        for username in usernames:
            for password in passwords:
                if results['successful_attempts'] >= max_attempts:
                    break

                try:
                    # Préparation des données
                    payload = {
                        username_field: username,
                        password_field: password
                    }

                    if csrf_token:
                        payload['csrf_token'] = csrf_token

                    headers = {
                        'Content-Type': content_type,
                        'Accept': 'text/html,application/json'
                    }

                    # Envoi de la requête
                    response = session.post(url, data=payload, headers=headers, allow_redirects=False)

                    # Analyse de la réponse
                    auth_successful = self._check_auth_success(response, session)

                    results['tested_credentials'].append({
                        'username': username,
                        'password': password,
                        'success': auth_successful,
                        'status_code': response.status_code,
                        'response_url': response.headers.get('Location', '')
                    })

                    if auth_successful:
                        results['successful_attempts'] += 1
                        results['vulnerable'] = True
                        module_results.append({
                            'message': 'Authentification réussie détectée',
                            'vulnerable': True,
                            'credentials': {
                                username_field: username,
                                password_field: password
                            }
                        })
                        break
                    else:
                        results['failed_attempts'] += 1

                    time.sleep(delay)

                except Exception as e:
                    logging.error(f"Erreur lors du test: {str(e)}")
                    results['errors'].append(str(e))

        if not results['vulnerable']:
            module_results.append({
                'message': 'Aucune authentification réussie détectée',
                'vulnerable': False,
                'details': results
            })

        context['module_results'] = module_results
        return context

    @staticmethod
    def _extract_csrf_token(html_content):
        """Extrait le token CSRF du formulaire HTML."""
        import re
        csrf_pattern = r'name="csrf_token" value="([^"]+)"'
        match = re.search(csrf_pattern, html_content)
        return match.group(1) if match else None

    @staticmethod
    def _check_auth_success(response, session):
        """
        Vérifie si l'authentification a réussi en utilisant plusieurs indicateurs :
        1. Code de statut de redirection (302, 303, 307)
        2. Présence d'URL de redirection vers le dashboard
        3. Accès réussi à la page de destination
        4. Présence de cookies de session
        """
        # Vérification du code de statut
        if response.status_code in (301, 302, 303, 307):
            redirect_url = response.headers.get('Location')
            if redirect_url and ('/dashboard' in redirect_url or '/profile' in redirect_url):
                try:
                    # Tenter d'accéder à la page de redirection
                    redirect_response = session.get(redirect_url, allow_redirects=False)
                    return redirect_response.status_code == 200
                except:
                    pass

        # Vérification des cookies de session
        session_cookies = session.cookies.get_dict()
        return bool(session_cookies.get('session') or session_cookies.get('remember_token'))