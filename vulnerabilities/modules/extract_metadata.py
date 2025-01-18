import requests
from bs4 import BeautifulSoup
from base_module import BaseModule

class Module(BaseModule):
    def run(self, context):
        """
        Extrait les métadonnées sensibles d'une page web
        """
        url = context.get('url', context.get('target'))
        module_results = context.setdefault('module_results', [])
        metadata_results = {
            'sensitive_headers': [],
            'comments': [],
            'sensitive_scripts': []
        }

        if not url:
            module_results.append({
                'Metadata Analysis': {
                    'error': 'Aucune URL fournie'
                }
            })
            return context

        try:
            response = requests.get(url)
            
            # Analyse des en-têtes
            sensitive_headers = ['server', 'x-powered-by', 'via']
            for key, value in response.headers.items():
                if key.lower() in sensitive_headers:
                    metadata_results['sensitive_headers'].append({
                        'header': key,
                        'value': value
                    })

            # Analyse du contenu HTML
            soup = BeautifulSoup(response.text, 'html.parser')

            # Recherche des commentaires
            comments = soup.find_all(text=lambda text: isinstance(text, str) and '<!--' in text)
            for comment in comments:
                metadata_results['comments'].append({
                    'content': str(comment),
                    'type': 'HTML comment'
                })

            # Analyse des scripts
            scripts = soup.find_all('script')
            sensitive_keywords = ['config', 'credentials', 'api', 'key', 'secret']
            for script in scripts:
                if script.string:
                    for keyword in sensitive_keywords:
                        if keyword in script.string.lower():
                            metadata_results['sensitive_scripts'].append({
                                'keyword': keyword,
                                'script_preview': script.string[:100] + '...'
                            })

            # Ajout des résultats au context
            module_results.append({
                'Metadata Analysis': {
                    'url': url,
                    'status': 'completed',
                    'findings': metadata_results,
                    'vulnerable': (
                        len(metadata_results['sensitive_headers']) > 0 or
                        len(metadata_results['comments']) > 0 or
                        len(metadata_results['sensitive_scripts']) > 0
                    )
                }
            })

        except requests.exceptions.RequestException as e:
            module_results.append({
                'Metadata Analysis': {
                    'url': url,
                    'status': 'error',
                    'error_message': str(e)
                }
            })

        return context
