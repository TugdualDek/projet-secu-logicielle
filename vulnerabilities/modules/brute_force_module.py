import requests
import time
from datetime import datetime
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from vulnerabilities.modules.base_module import BaseModule
from vulnerabilities.modules.anti_bruteforce_detector import DefaultAntiBruteforceDetector
from vulnerabilities.modules.credential_provider import DefaultCredentialProvider

class Module(BaseModule):
    def __init__(
            self,
            credential_provider=None,
            anti_bruteforce_detector=None
    ):
        self.credential_provider = credential_provider
        self.anti_bruteforce_detector = anti_bruteforce_detector
        self.initial_page_content = None
        self.initial_url = None

    def _get_form_fields(self, login_endpoint):
        """Extrait les champs du formulaire et leurs types"""
        form_fields = {
            'username_field': None,
            'password_field': None,
            'token_field': None,
            'submit_field': None
        }

        for input_field in login_endpoint.get('inputs', []):
            input_type = input_field.get('type', '').lower()
            input_name = input_field.get('name')

            if input_type == 'text' or input_type == 'email':
                form_fields['username_field'] = input_name
            elif input_type == 'password':
                form_fields['password_field'] = input_name
            elif input_type == 'hidden':
                form_fields['token_field'] = input_name
            elif input_type == 'submit':
                form_fields['submit_field'] = input_name

        return form_fields

    def _is_success(self, response, initial_response, session):
        """
        Détecte si la connexion est réussie
        """
        if not response or not initial_response:
            return False

        response_lower = response.text.lower()
        initial_lower = initial_response.lower()

        # 1. Vérifier le changement d'URL
        if response.url != self.initial_url:
            return True

        # 2. Rechercher des indicateurs clairs de succès
        success_indicators = [
            'welcome', 'logout', 'dashboard', 'profile',
            'successfully', 'logged in', 'security level',
            'dvwa security'
        ]
        if any(indicator in response_lower for indicator in success_indicators):
            return True

        # 3. Rechercher des messages d'erreur communs
        error_indicators = [
            'invalid', 'incorrect', 'failed', 'error',
            'wrong password', 'wrong username',
            'login failed', 'try again'
        ]
        has_errors = any(indicator in response_lower for indicator in error_indicators)
        if has_errors:
            return False

        # 4. Vérifier les changements majeurs de contenu
        if abs(len(response.text) - len(initial_response)) > (len(initial_response) * 0.3):
            return True

        # 5. Vérifier l'apparition/disparition d'éléments clés
        if '<form' in initial_lower and '<form' not in response_lower:
            return True

        # 6. Vérifier l'apparition de nouveaux cookies de session
        initial_cookies = {c.name for c in session.cookies}
        new_cookies = {c.name for c in response.cookies}
        if new_cookies - initial_cookies:
            return True

        return False
    def run(self, context):
        """
        Point d'entrée principal du module.
        """
        login_endpoint = context.get('login_endpoint')
        if not login_endpoint:
            context.setdefault('errors', []).append("Aucun endpoint de login trouvé")
            context.setdefault('module_results', []).append({
                'Brute Force': {
                    'error': "Aucun endpoint de login trouvé"
                }
            })
            return context

        # Initialiser les détecteurs et providers
        provider = self.credential_provider or DefaultCredentialProvider()
        detector = self.anti_bruteforce_detector or DefaultAntiBruteforceDetector()

        # Créer une session pour gérer les cookies et le CSRF
        session = requests.Session()

        # Obtenir les champs du formulaire
        form_fields = self._get_form_fields(login_endpoint)

        # Paramètres de base
        max_attempts = context.get('max_attempts', 20)
        base_delay = context.get('delay', 1)

        # Structure pour stocker les résultats
        results = {
            'tested_combinations': [],
            'successful_attempts': [],
            'failed_attempts': 0,
            'protection_detected': None,
            'errors': []
        }

        try:
            # Obtenir la page initiale pour comparaison
            initial_response = session.get(login_endpoint['url'])
            self.initial_page_content = initial_response.text
            self.initial_url = initial_response.url

            # Pour chaque combinaison d'identifiants
            for username, password in provider.get_credentials(context):
                if results['failed_attempts'] >= max_attempts:
                    break

                try:
                    # Récupérer un nouveau token CSRF pour chaque tentative
                    form_response = session.get(login_endpoint['url'])
                    soup = BeautifulSoup(form_response.text, 'html.parser')

                    # Construire le payload
                    payload = {
                        form_fields['username_field']: username,
                        form_fields['password_field']: password
                    }

                    # Ajouter le token CSRF s'il existe
                    if form_fields['token_field']:
                        token_input = soup.find('input', {'name': form_fields['token_field']})
                        if token_input:
                            payload[form_fields['token_field']] = token_input.get('value')

                    # Ajouter le champ submit s'il existe
                    if form_fields['submit_field']:
                        payload[form_fields['submit_field']] = 'Login'

                    # Faire la tentative de connexion
                    response = session.post(
                        login_endpoint['url'],
                        data=payload,
                        allow_redirects=True
                    )

                    # Vérifier si la connexion est réussie
                    success = self._is_success(response, self.initial_page_content, session)

                    # Enregistrer la tentative
                    attempt_info = {
                        'username': username,
                        'password': password,
                        'success': success,
                        'status_code': response.status_code
                    }

                    results['tested_combinations'].append(attempt_info)

                    if success:
                        results['successful_attempts'].append(attempt_info)
                        break
                    else:
                        results['failed_attempts'] += 1

                    # Vérifier les protections anti-bruteforce
                    protection_type = detector.detect(response)
                    if protection_type:
                        strategy = detector.adjust_strategy(protection_type)
                        results['protection_detected'] = protection_type

                        if strategy['action'] == 'abort':
                            break
                        elif strategy['action'] == 'wait':
                            time.sleep(strategy['delay'])
                            max_attempts = min(max_attempts, strategy['max_attempts'])
                    else:
                        # Délai adaptatif
                        time.sleep(base_delay * (1 + results['failed_attempts'] * 0.1))

                except requests.RequestException as e:
                    error_msg = f"Erreur lors de la tentative {username}:{password} : {str(e)}"
                    results['errors'].append(error_msg)

        except Exception as e:
            results['errors'].append(f"Erreur générale : {str(e)}")

        if results['successful_attempts']:
            final_message = "Brute force successful!"
            context['brute_force_results'] = {
                'message': final_message,
                'details': results,
                'vulnerable': True
            }
        else:
            final_message = "No successful brute force attempt."
            context['brute_force_results'] = {
                'message': final_message,
                'details': results,
                'vulnerable': False
            }

            # Pour le module results_saver
        context.setdefault('module_results', []).append({
            'Brute Force Results': context['brute_force_results']
        })

        return context