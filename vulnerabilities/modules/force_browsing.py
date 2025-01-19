import requests
from urllib.parse import urljoin
from base_module import BaseModule

class Module(BaseModule):
    def run(self, context):
        target_url = context.get('url')
        paths_url = context.get('paths_url')
        module_results = []

        if not target_url:
            module_results.append({'error': 'Aucune URL cible fournie.'})
            context['module_results'] = module_results
            return context

        if not paths_url:
            module_results.append({'error': 'Aucune URL de liste de chemins fournie.'})
            context['module_results'] = module_results
            return context

        try:
            response = requests.get(paths_url, timeout=10)
            if response.status_code != 200:
                module_results.append({'error': f"Impossible de récupérer les chemins depuis {paths_url}."})
                context['module_results'] = module_results
                return context
            paths_to_check = response.text.splitlines()
        except requests.RequestException as e:
            module_results.append({'error': f"Erreur lors de la récupération de la liste des chemins : {e}"})
            context['module_results'] = module_results
            return context

        for path in paths_to_check:
            full_url = urljoin(target_url, path.strip())
            try:
                response = requests.get(full_url, timeout=10)
                status_code = response.status_code

                if status_code == 200:
                    module_results.append({
                        'url': full_url,
                        'status_code': status_code,
                        'accessible': True,
                        'vulnerable': True
                    })
                    context['module_results'] = module_results
                    return context
                else:
                    print(f"{full_url} -> {status_code}")

            except requests.RequestException as e:
                module_results.append({
                    'url': full_url,
                    'error': str(e),
                    'accessible': False
                })

        if not module_results:
            module_results.append({'message': 'Aucune ressource vulnérable trouvée.'})

        context['module_results'] = module_results
        return context