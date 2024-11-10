from base_module import BaseModule
import requests
from requests.exceptions import RequestException

class Module(BaseModule):
    def run(self, context):
        url = context.get('url')
        if not url:
            context['error'] = "L'URL n'est pas spécifiée dans le contexte."
            return context

        timeout = context.get('timeout', 5)

        # Validation du timeout
        try:
            timeout = float(timeout)
            if timeout <= 0:
                raise ValueError()
        except (ValueError, TypeError):
            timeout = 5

        try:
            response = requests.get(url, timeout=timeout)
            context['response'] = response
        except RequestException as e:
            context['error'] = f"Échec de la requête HTTP : {e}"

        return context
