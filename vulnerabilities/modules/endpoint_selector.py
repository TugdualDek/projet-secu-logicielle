from vulnerabilities.modules.base_module import BaseModule


class Module(BaseModule):
    def run(self, context):
        # Récupération des endpoints découverts
        endpoints = context.get('discovered_endpoints', [])

        # Mots-clés par défaut pour URL et champs si rien n'est fourni dans le contexte
        default_auth_url_keywords = ['login', 'signin', 'auth', 'connexion', 'connect', 'logon']
        default_username_field_keywords = ['user', 'username', 'email', 'mail', 'identifier', 'login']
        default_password_field_keywords = ['pass', 'password', 'pwd', 'passwd']

        # Récupération des mots-clés depuis le contexte ou utilisation des valeurs par défaut
        auth_url_keywords = context.get('auth_url_keywords', default_auth_url_keywords)
        username_field_keywords = context.get('username_field_keywords', default_username_field_keywords)
        password_field_keywords = context.get('password_field_keywords', default_password_field_keywords)

        login_endpoint = None

        for ep in endpoints:
            url = (ep.get('url') or '').lower()
            inputs = ep.get('inputs', [])

            # 1. Vérification de l'URL : si l'un des mots-clés d'authentification apparaît dans l'URL
            url_matches_auth = any(keyword in url for keyword in auth_url_keywords)

            # 2. Vérification des champs du formulaire :
            #    - On cherche un champ qui ressemble à un champ utilisateur (username/email)
            #    - On cherche un champ mot de passe
            fields = { (input_field.get('name') or '').lower(): input_field.get('type', '').lower() for input_field in inputs if input_field.get('name') }

            # On considère qu'un champ utilisateur est présent s'il y a un input dont le nom contient l'un des username_field_keywords
            # ou si le type est "text" (ou similaire) et que son nom est proche d'un pattern utilisateur.
            user_field_detected = any(
                any(keyword in field_name for keyword in username_field_keywords)
                for field_name in fields.keys()
            )

            # Un champ password est présent si le type est password ou si le nom du champ contient les mots-clés liés au mot de passe
            password_field_detected = any(
                (field_type == 'password') or any(keyword in field_name for keyword in password_field_keywords)
                for field_name, field_type in fields.items()
            )

            # Critères de sélection d'un endpoint de connexion :
            # - Si l'URL contient un mot-clé d'auth
            # - ET un champ password est présent
            # OU
            # - Le formulaire contient des champs "username" + "password" même si l'URL n'est pas explicite
            if (url_matches_auth and password_field_detected) or (user_field_detected and password_field_detected):
                login_endpoint = ep
                break

        if login_endpoint:
            context['login_endpoint'] = login_endpoint
        else:
            context.setdefault('errors', []).append("Aucun endpoint de connexion détecté avec les mots-clés fournis.")

        return context
