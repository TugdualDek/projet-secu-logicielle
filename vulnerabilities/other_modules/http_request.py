from vulnerabilities.modules.base_module import BaseModule
import requests

class Module(BaseModule):
    def run(self, context):
        url = context.get('url')
        timeout = context.get('timeout', 5)
        try:
            response = requests.get(url, timeout=timeout)
            # Stocker uniquement les en-têtes nécessaires pour les analyses suivantes
            context['response_headers'] = dict(response.headers)
            # Stock les cookies
            context['response_cookies'] = response.cookies
            # Vous pouvez stocker d'autres informations si nécessaire, par exemple :
            # context['status_code'] = response.status_code
            # context['response_content'] = response.text
        except requests.RequestException as e:
            context.setdefault('errors', []).append(f"Échec de la requête HTTP : {e}")
        return context