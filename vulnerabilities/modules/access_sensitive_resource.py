from base_module import BaseModule
import requests

class Module(BaseModule):
    def run(self, context):
        try:
            print("AccessSensitiveResource : Début de l’exécution")

            # Récupérer la session du contexte (qui peut être None si la connexion a échoué)
            session = context.get('session')
            url = context.get('target')

            if not url:
                raise ValueError("URL manquante dans le contexte pour envoyer la requête malveillante.")

            expected_result = context.get('expected_result')

            if not all([url, expected_result]):
                raise ValueError("Informations manquantes dans le contexte pour accéder à la ressource.")

            # Vérifier si expected_result a une valeur valide
            if expected_result not in ["allowed", "denied"]:
                # Définir access_result à False
                context['access_result'] = False
                # Définir un code d’erreur spécifique
                context['error_code'] = 'INVALID_EXPECTED_RESULT'
                # Ajouter un message d’erreur informatif
                context.setdefault('errors', []).append(
                    f"Valeur invalide pour expected_result : {expected_result}. "
                    f"Les valeurs valides sont 'allowed' et 'denied'."
                )
                return context

            print(f"AccessSensitiveResource : Tentative d’accès à {url}")
            response = session.get(url)
            print(f"AccessSensitiveResource : Code de statut de la réponse : {response.status_code}")

            if expected_result == "allowed":
                result = response.status_code == 200
            elif expected_result == "denied":
                result = response.status_code == 403
            else:
                result = False

            # Stocker le résultat dans le contexte
            context['access_result'] = result
            return context

        except requests.exceptions.RequestException as e:
            print(f"AccessSensitiveResource : Erreur de requête : {e}")
            context.setdefault('errors', []).append(f"Erreur de requête : {e}")
            return context
        except Exception as e:
            print(f"AccessSensitiveResource : Erreur inattendue : {e}")
            context.setdefault('errors', []).append(f"Erreur dans AccessSensitiveResource : {e}")
            return context