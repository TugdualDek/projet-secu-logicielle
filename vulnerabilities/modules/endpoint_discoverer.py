from vulnerabilities.modules.base_module import BaseModule
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import time

class Module(BaseModule):
    def run(self, context):
        start_url = context.get('url', context.get('target'))
        max_depth = context.get('max_depth', 20)
        delay = context.get('delay', 0.5)
        visited_urls = set()
        crawled_urls = []
        discovered_endpoints = []
        module_results = context.setdefault('module_results', [])

        if not start_url:
            module_results.append({'Endpoint Discovery': {'error': 'Aucune URL cible fournie'}})
            return context

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

        def crawl(url, depth):
            if depth > max_depth or url in visited_urls:
                return
            visited_urls.add(url)
            try:
                print(f"Attempting to crawl: {url}")
                response = requests.get(url, headers=headers, timeout=30)
                print(f"Response status code: {response.status_code}")
                if 'text/html' not in response.headers.get('Content-Type', ''):
                    print(f"Ignoring non-HTML content at {url}")
                    return
                soup = BeautifulSoup(response.text, 'html.parser')
                crawled_urls.append(url)
                forms = soup.find_all('form')
                for form in forms:
                    action = form.get('action')
                    method = form.get('method', 'get').lower()
                    inputs = form.find_all('input')
                    endpoint_info = {
                        'url': urljoin(url, action) if action else url,
                        'method': method,
                        'inputs': [{'name': input_tag.get('name'), 'type': input_tag.get('type', 'text')} for input_tag in inputs if input_tag.get('name')]
                    }
                    discovered_endpoints.append(endpoint_info)
                for link in soup.find_all('a', href=True):
                    absolute_link = urljoin(url, link['href'])
                    if urlparse(absolute_link).netloc == urlparse(start_url).netloc:
                        crawl(absolute_link, depth + 1)

                time.sleep(delay)

            except requests.RequestException as e:
                print(f"Request failed: {e}")
                module_results.append({'Endpoint Discovery': {'error': f"Échec de l'exploration de {url} : {e}"}})

        crawl(start_url, 0)
        context['crawled_urls'] = crawled_urls
        context['discovered_endpoints'] = discovered_endpoints

        if not crawled_urls:
            module_results.append({'Endpoint Discovery': {'message': 'Aucun URL découvert', 'vulnerable': False}})
        return context