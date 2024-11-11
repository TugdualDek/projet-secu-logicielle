from http.cookies import SimpleCookie
from base_module import BaseModule

class Module(BaseModule):
    def run(self, context):
        headers = context.get('response_headers')
        if not headers:
            context.setdefault('errors', []).append("Aucune en-tête trouvée pour l'analyse des cookies.")
            return context

        cookies = headers.get('Set-Cookie')
        if not cookies:
            context.setdefault('results', {})['cookies_analysis'] = "Aucun cookie trouvé."
            return context

        cookie_parser = SimpleCookie()
        cookie_parser.load(cookies)

        results = {}
        for morsel in cookie_parser.values():
            cookie_name = morsel.key
            attributes = {
                'Secure': 'secure' in morsel.get('secure', '').lower(),
                'HttpOnly': 'httponly' in morsel.get('httponly', '').lower(),
                'SameSite': morsel.get('samesite') or 'None'
            }
            results[cookie_name] = attributes

        context.setdefault('results', {})['cookies_analysis'] = results
        return context
