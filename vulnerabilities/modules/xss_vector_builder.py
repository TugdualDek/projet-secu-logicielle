from urllib.parse import urlparse, parse_qs, urlencode, urlunparse, urljoin
from base_module import BaseModule

class Module(BaseModule):
    def run(self, context):
        crawled_urls = context.get('crawled_urls', [])
        discovered_forms = context.get('discovered_forms', [])
        xss_payloads = context.get('xss_payloads', [])
        injection_vectors = []

        for url_str in crawled_urls:
            parsed_url = urlparse(url_str)
            query_params = parse_qs(parsed_url.query)

            for param in query_params:
                for payload in xss_payloads:
                    modified_params = query_params.copy()
                    modified_params[param] = payload
                    new_query = urlencode(modified_params, doseq=True)
                    new_url = urlunparse(parsed_url._replace(query=new_query))
                    injection_vectors.append({
                        'method': 'get',
                        'url': new_url,
                        'params': None
                    })

        for form in discovered_forms:
            action = form.get('action', '')
            method = form.get('method', 'get').lower()
            if not action:
                action = '/'
            form_url = urljoin(context.get('url', ''), action)

            for payload in xss_payloads:
                form_data = {}
                for input_field in form['inputs']:
                    if input_field['type'] in ['text', 'search', 'email', 'password', 'url']:
                        form_data[input_field['name']] = payload
                    else:
                        form_data[input_field['name']] = 'test'

                injection_vectors.append({
                    'method': method,
                    'url': form_url,
                    'data': form_data if method == 'post' else None,
                    'params': form_data if method == 'get' else None
                })

        context['injection_vectors'] = injection_vectors
        return context
