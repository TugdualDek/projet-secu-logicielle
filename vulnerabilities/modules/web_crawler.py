import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import time

class Module:
    def run(self, context):
        start_url = context.get('url')
        max_depth = context.get('max_depth', 2)
        delay = context.get('delay', 0.5)
        visited_urls = set()
        crawled_urls = []
        discovered_forms = []

        if not start_url:
            context['errors'] = 'Aucune URL cible fournie'
            return context

        def crawl(url, depth):
            if depth > max_depth or url in visited_urls:
                return
            visited_urls.add(url)

            try:
                response = requests.get(url, timeout=5)
                if 'text/html' not in response.headers.get('Content-Type', ''):
                    return

                soup = BeautifulSoup(response.text, 'html.parser')
                forms = soup.find_all('form')
                for form in forms:
                    form_details = self.parse_form(form, url)
                    discovered_forms.append(form_details)

                for link in soup.find_all('a', href=True):
                    absolute_link = urljoin(url, link['href'])
                    if urlparse(absolute_link).netloc == urlparse(start_url).netloc:
                        crawled_urls.append(absolute_link)
                        crawl(absolute_link, depth + 1)

                time.sleep(delay)

            except requests.RequestException as e:
                context.setdefault('errors', []).append(f"Erreur lors de la requête {url}: {e}")

        self.parse_form = lambda form, base_url: {
            'action': urljoin(base_url, form.get('action')),
            'method': form.get('method', 'get').lower(),
            'inputs': [
                {'name': input_tag.get('name'), 'type': input_tag.get('type', 'text')}
                for input_tag in form.find_all('input')
                if input_tag.get('name')
            ]
        }

        crawl(start_url, 0)
        context['crawled_urls'] = list(visited_urls)
        context['discovered_forms'] = discovered_forms
        return context