import requests
from urllib.parse import urljoin
from base_module import BaseModule

class Module(BaseModule):
    def run(self, context):
        target_url = context.get('url')
        paths_to_check = context.get('paths', [])
        module_results = []

        if not target_url:
            module_results.append({'error': 'Aucune URL cible fournie.'})
            context['module_results'] = module_results
            return context

        if not paths_to_check:
            module_results.append({'error': 'Aucun chemin à tester fourni.'})
            context['module_results'] = module_results
            return context

        for path in paths_to_check:
            full_url = urljoin(target_url, path)
            try:
                response = requests.get(full_url, timeout=20)
                status_code = response.status_code
                if status_code == 200:
                    module_results.append({
                        'url': full_url,
                        'status_code': status_code,
                        'accessible': True
                    })
                else:
                    print(f"{full_url} -> {status_code}")
            except requests.RequestException as e:
                module_results.append({
                    'url': full_url,
                    'error': str(e),
                    'accessible': False
                })

        if not module_results:
            module_results.append({'message': 'Aucune ressource trouvée.'})

        context['module_results'] = module_results
        return context