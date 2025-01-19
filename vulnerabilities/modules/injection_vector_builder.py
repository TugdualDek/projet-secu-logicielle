from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
from base_module import BaseModule

class Module(BaseModule):
    def run(self, context):
        urls = context.get('crawled_urls', [])
        forms = context.get('discovered_forms', [])
        sql_payloads = context.get('sql_payloads', [])
        injection_vectors = []

        for url_str in urls:
            parsed_url = urlparse(url_str)
            query_params = parse_qs(parsed_url.query)

            for param in query_params:
                for payload in sql_payloads:
                    modified_params = query_params.copy()
                    modified_params[param] = payload
                    new_query = urlencode(modified_params, doseq=True)
                    new_url = urlunparse(parsed_url._replace(query=new_query))
                    injection_vectors.append({
                        'method': 'get',
                        'url': new_url,
                        'params': None
                    })

        for form in forms:
            for payload in sql_payloads:
                form_data = {}
                for input_field in form['inputs']:
                    if input_field['type'] in ['text', 'search', 'email', 'password']:
                        form_data[input_field['name']] = payload
                    else:
                        form_data[input_field['name']] = 'test'

                injection_vectors.append({
                    'method': form['method'],
                    'url': form['action'],
                    'data': form_data if form['method'] == 'post' else None,
                    'params': form_data if form['method'] == 'get' else None
                })

        context['injection_vectors'] = injection_vectors
        return context