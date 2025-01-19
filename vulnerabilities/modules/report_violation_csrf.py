from base_module import BaseModule
import json

class Module(BaseModule):
    def run(self, context):
        try:
            # Retrieve information from the context
            vulnerable_url = context.get('target')
            if not vulnerable_url:
                raise ValueError("URL missing in the context to report the CSRF violation.")

            violation_type = context.get('violation_type', 'csrf')
            details = context.get('details', '')
            request_status = context.get('request_status')
            response_content = context.get('response_content')
            attack_value = context.get('attack_value')
            errors = context.get('errors', [])  # Retrieve the list of errors

            # Create the results dictionary
            result = {}

            if request_status == 200 and attack_value in response_content:
                result = {
                    'vulnerability_type': violation_type,
                    'vulnerable_url': vulnerable_url,
                    'details': 'CSRF vulnerability detected!',
                    'request_response_data': {  # Include request and response data
                        'request_headers': context.get('request_headers'),
                        'request_body': context.get('request_body'),
                        'response_headers': context.get('response_headers'),
                        'response_body': context.get('response_body')
                    }
                }
                if details:
                    result['details'] = details
            else:
                result = {
                    'vulnerability_type': violation_type,
                    'vulnerable_url': vulnerable_url,
                    'details': 'No CSRF vulnerability detected.',
                    'errors': errors,  # Include error messages if no vulnerability is found
                }

            # Create the final result
            final_result = {
                'vulnerability_type': violation_type,
                'vulnerability_name': 'CSRF Vulnerability',
                'description': json.dumps(result, indent=2, ensure_ascii=False),
                'additional_info': {
                    'recommendations': [
                        'Implement anti-CSRF tokens.',
                        'Enable HTTP Strict Transport Security (HSTS).',
                        'Use a web application firewall (WAF).'
                    ]
                }
            }

            # Store in context['results'] as a list
            context['results'] = [final_result]

            return context

        except Exception as e:
            context.setdefault('errors', []).append(f"Error in report_violation_csrf : {e}")
            return context