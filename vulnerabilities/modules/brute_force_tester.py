from base_module import BaseModule
import requests
import time
import logging
from bs4 import BeautifulSoup

class Module(BaseModule):
    def run(self, context):
        login_endpoint = context.get('login_endpoint')
        if not login_endpoint:
            return {
                'message': 'Aucun endpoint de login trouvé',
                'vulnerable': False
            }

        url = login_endpoint['url']
        method = login_endpoint['method']
        content_type = context.get('content_type', 'application/x-www-form-urlencoded')
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

        session = requests.Session()

        for username in usernames:
            for password in passwords:
                if results['successful_attempts'] >= max_attempts:
                    break

                try:
                    # 1. Récupérer la page de login pour obtenir un nouveau token CSRF
                    initial_response = session.get(url)
                    if initial_response.status_code != 200:
                        error_msg = f"Erreur lors de la récupération de la page de login: {initial_response.status_code}"
                        logging.error(error_msg)
                        results['errors'].append(error_msg)
                        continue

                    # Utiliser BeautifulSoup pour extraire le token
                    csrf_token = self._extract_csrf_token(initial_response.text)
                    if not csrf_token:
                        error_msg = "Impossible d'obtenir le token CSRF"
                        logging.error(error_msg)
                        results['errors'].append(error_msg)
                        continue

                    # 2. Préparation des données avec le token CSRF
                    payload = {
                        'csrf_token': csrf_token,
                        username_field: username,
                        password_field: password,
                        'remember_me': 'y'
                    }

                    headers = {'Content-Type': content_type,
                               'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                               'Referer': url}

                    # Ajouter le referer qui est l'URL de la page de login

                    # 3. Envoi de la requête d'authentification
                    response = session.post(
                        url=url,
                        data=payload,
                        headers=headers,
                        allow_redirects=True,
                        timeout=10
                    )

                    # 4. Analyse de la réponse pour détecter une authentification réussie
                    auth_successful = self._check_auth_success(response)

                    results['tested_credentials'].append({
                        'username': username,
                        'password': password,
                        'success': auth_successful,
                        'status_code': response.status_code,
                        'response_url': response.url
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
                    else:
                        results['failed_attempts'] += 1

                    time.sleep(delay)

                except Exception as e:
                    error_msg = f"Erreur lors du test: {str(e)}"
                    logging.error(error_msg)
                    results['errors'].append(error_msg)

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
        """
        Extrait le token CSRF du formulaire HTML en utilisant BeautifulSoup.
        :param html_content: Contenu HTML de la page
        :return: Token CSRF ou None si non trouvé
        """
        try:
            soup = BeautifulSoup(html_content, 'html.parser')
            # Chercher spécifiquement l'input avec name="csrf_token"
            csrf_input = soup.find('input', {'name': 'csrf_token'})
            if csrf_input and csrf_input.has_attr('value'):
                return csrf_input['value']
        except Exception as e:
            logging.error(f"Erreur lors de l'extraction du token CSRF: {e}")
        return None

    @staticmethod
    def _check_auth_success(response):
        """
        Vérifie si l'authentification a réussi.
        :param response: Réponse de la requête
        :return: Boolean indiquant si l'authentification a réussi
        """
        # En cas de redirection vers dashboard/profile, c'est un succès
        if response.status_code == 302 and ('/dashboard' in response.url or '/profile' in response.url):
            return True

        # Si on arrive sur dashboard/profile après redirection, c'est un succès
        if response.url and ('/dashboard' in response.url or '/profile' in response.url):
            return True

        return False