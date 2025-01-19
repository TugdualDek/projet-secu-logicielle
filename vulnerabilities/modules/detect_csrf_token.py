from base_module import BaseModule
import requests

class Module(BaseModule):
    def run(self, context):
        try:
            url = context.get('target')

            if not url:
                raise ValueError("URL manquante dans le contexte pour détecter le jeton CSRF.")

            response = requests.get(url)
            headers = response.headers
            cookies = response.cookies

            common_token_names = ['csrf_token', 'csrftoken', 'xsrf_token', 'authenticity_token']

            token = None
            for header_name, header_value in headers.items():
                if header_name.lower() in common_token_names:
                    token = header_value
                    break

            if not token:
                for cookie_name, cookie_value in cookies.items():
                    if cookie_name.lower() in common_token_names:
                        token = cookie_value
                        break

            if token:
                context['csrf_token'] = token

            return context

        except requests.exceptions.RequestException as e:
            context.setdefault('errors', []).append(f"Erreur lors de la requête pour détecter le jeton CSRF : {e}")
            return context
        except Exception as e:
            context.setdefault('errors', []).append(f"Erreur dans detect_csrf_token : {e}")
            return context