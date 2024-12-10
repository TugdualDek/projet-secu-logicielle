import requests
import time
import re

class Module:
    def run(self, context):
        injection_vectors = context.get('injection_vectors', [])
        sql_payloads = context.get('sql_payloads', [])
        module_results = []

        error_signatures = [
            'you have an error in your sql syntax',
            'warning: mysql',
            'unclosed quotation mark after the character string',
            'quoted string not properly terminated',
            'invalid query',
            'sql syntax',
            'odbc drivers error',
            'Warning: mysql'
        ]

        for vector in injection_vectors:
            url = vector.get('url')
            method = vector.get('method', 'get')
            params = vector.get('params')
            data = vector.get('data')
            for payload in sql_payloads:
                test_params = {key: f"{value}{payload}" for key, value in (params or {}).items()}
                test_data = {key: f"{value}{payload}" for key, value in (data or {}).items()}
                try:
                    start_time = time.time()
                    if method == 'get':
                        response = requests.get(url, params=test_params, timeout=10)
                    elif method == 'post':
                        response = requests.post(url, data=test_data, timeout=10)
                    else:
                        continue

                    end_time = time.time()
                    response_time = end_time - start_time
                    for signature in error_signatures:
                        if re.search(signature, response.text, re.IGNORECASE):
                            module_results.append({
                                'url': url,
                                'method': method.upper(),
                                'payload': payload,
                                'error_signature': signature,
                                'vulnerable': True,
                                'type': 'Error-Based SQL Injection'
                            })
                            break
                    if 'sleep' in payload and response_time > 5:
                        module_results.append({
                            'url': url,
                            'method': method.upper(),
                            'payload': payload,
                            'response_time': response_time,
                            'vulnerable': True,
                            'type': 'Time-Based Blind SQL Injection'
                        })
                except requests.RequestException as e:
                    module_results.append({
                        'url': url,
                        'error': str(e),
                        'vulnerable': False
                    })

        if not module_results:
            module_results.append({
                'message': 'No SQL injection vulnerabilities detected',
                'vulnerable': False
            })

        context['module_results'] = module_results
        return context
