# endpoint_discoverer.py

from base_module import BaseModule
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, parse_qs
import time

class Module(BaseModule):
    def run(self, context):
        start_url = context.get('url', context.get('target'))
        max_depth = context.get('max_depth', 2)
        delay = context.get('delay', 0.5)  # Délai entre les requêtes en secondes
        visited_urls = set()
        discovered_endpoints = []
        module_results = context.setdefault('module_results', [])

        # Vérifier que l'URL de départ est valide
        if not start_url:
            module_results.append({
                'Endpoint Discovery': {
                    'error': 'Aucune URL cible fournie'
                }
            })
            return context

        def crawl(url, depth):
            if depth > max_depth or url in visited_urls:
                return
            visited_urls.add(url)
            try:
                response = requests.get(url, timeout=5)
                content_type = response.headers.get('Content-Type', '')
        
                # Vérifier le code de statut HTTP
                if response.status_code != 200:
                    print(f"Skipping URL {url} due to status code {response.status_code}")
                    return
        
                # Vérifier le type de contenu
                if not content_type.startswith('text/html'):
                    print(f"Ignoring non-HTML content at {url}")
                    return  # Ignorer les ressources non HTML
        
                # Utiliser response.text au lieu de response.content
                soup = BeautifulSoup(response.text, 'html.parser')

                # Extraire et traiter les formulaires
                forms = soup.find_all('form')
                for form in forms:
                    action = form.get('action')
                    method = form.get('method', 'get').lower()
                    inputs = form.find_all('input')

                    for input_tag in inputs:
                        input_type = input_tag.get('type', 'text')
                        input_name = input_tag.get('name')

                        if input_name and input_type in ['text', 'url', 'search']:
                            endpoint_info = {
                                'url': urljoin(url, action) if action else url,
                                'method': method,
                                'param_name': input_name
                            }
                            discovered_endpoints.append(endpoint_info)

                # Extraire et traiter les liens
                links = soup.find_all('a', href=True)
                for link in links:
                    href = link['href']
                    absolute_link = urljoin(url, href)
                    parsed_link = urlparse(absolute_link)

                    # Rester dans le même domaine
                    if parsed_link.netloc == urlparse(start_url).netloc:
                        # Vérifier les paramètres de requête
                        if parsed_link.query:
                            params = dict(parse_qs(parsed_link.query))
                            endpoint_info = {
                                'url': absolute_link.split('?')[0],
                                'method': 'get',
                                'params': {k: v[0] for k, v in params.items()}
                            }
                            discovered_endpoints.append(endpoint_info)

                        # Continuer le crawl récursivement
                        if absolute_link not in visited_urls:
                            crawl(absolute_link, depth + 1)

                time.sleep(delay)  # Respecter le serveur cible

            except requests.RequestException as e:
                module_results.append({
                    'Endpoint Discovery': {
                        'error': f"Échec de l'exploration de {url} : {e}"
                    }
                })

        # Démarrer l'exploration depuis l'URL initiale
        crawl(start_url, depth=0)

        # Stocker les endpoints découverts dans le contexte
        context['discovered_endpoints'] = discovered_endpoints

        #si aucun endpoint n'est découvert
        if not discovered_endpoints:
            module_results.append({
                'Endpoint Discovery': {
                    'message': 'Aucun endpoint découvert'
                }
            })

        return context
