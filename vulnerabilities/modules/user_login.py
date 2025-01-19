from base_module import BaseModule
import requests

class Module(BaseModule):
    def run(self, context):
        try:
            print("UserLogin : Début de l’exécution")
            session = requests.Session()
            url = context.get('target')
            if not url:
                raise ValueError("URL manquante dans le contexte pour envoyer la requête malveillante.")

            username = context.get('username')
            password = context.get('password')

            if not username or not password:
                raise ValueError("Nom d’utilisateur ou mot de passe manquant dans le contexte.")

            data = {
                "username": username,
                "password": password,
            }

            print(f"UserLogin : Tentative de connexion avec l’utilisateur {username}")
            response = session.post(url, data=data)  # Vérifiez la méthode HTTP (POST)
            print(f"UserLogin : Code de statut de la réponse : {response.status_code}")

            # Toujours stocker la session dans le contexte
            context['session'] = session

            if response.status_code == 200:
                print("UserLogin : Connexion réussie")
            else:
                print("UserLogin : Échec de la connexion")
                context.setdefault('errors', []).append(
                    f"Erreur de connexion pour l’utilisateur {username}. Code de statut : {response.status_code}"
                )

            return context

        except requests.exceptions.RequestException as e:
            print(f"UserLogin : Erreur de requête : {e}")
            context.setdefault('errors', []).append(f"Erreur de requête : {e}")
            return context
        except Exception as e:
            print(f"UserLogin : Erreur inattendue : {e}")
            context.setdefault('errors', []).append(f"Erreur dans UserLogin : {e}")
            return context
