from http.cookies import SimpleCookie
from vulnerabilities.modules.base_module import BaseModule

class Module(BaseModule):
    def run(self, context):
        cookies = context.get('response_cookies')
        module_results = context.setdefault('module_results', [])
        if not cookies:
            module_results.append({
                'Cookies Analysis': {
                    'error': 'No cookies found in the response'
                }
            })
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

        module_results.append({
            'Cookies Analysis': results
        })
        return context
