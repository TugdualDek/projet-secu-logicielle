from base_module import BaseModule
import json

class Module(BaseModule):
    def run(self, context):
        try:
            # Get information from the context
            violation_type = context.get('violation_type', 'least_privilege')
            username = context.get('username')
            url = context.get('target')
            if not url:
                raise ValueError("URL missing in the context to send the malicious request.")
            access_result = context.get('access_result')
            error_code = context.get('error_code')  # Retrieve the error code
            errors = context.get('errors', [])  # Retrieve the list of errors

            if not all([username, url, access_result]):
                raise ValueError("Missing information in the context to generate the report.")

            # Create the results dictionary
            result = {}

            if error_code:  # Check if an error code is present
                result = {
                    'violation_type': violation_type,
                    'username': username,
                    'resource_url': url,
                    'details': 'Error during the least privilege check.',  # Changed to English
                    'error_code': error_code,  # Include the error code in the result
                    'error_messages': errors  # Include error messages
                }
            elif access_result:  # If no error and access is allowed
                result = {
                    'violation_type': violation_type,
                    'username': username,
                    'resource_url': url,
                    'details': 'Violation of the least privilege principle detected!',  # Changed to English
                    'session_info': {  # Include session information
                        'session_id': context.get('session', {}).get('session_id'),
                        'expiry_date': context.get('session', {}).get('expiry_date')
                    }
                }
            else:  # If no error and access is denied
                if any("Erreur de connexion" in err for err in errors):
                    result = {
                        'violation_type': violation_type,
                        'username': username,
                        'resource_url': url,
                        'details': 'Potential vulnerability: Access granted despite a login error.',  # Changed to English
                        'request_response_data': {  # Include request and response data
                            'request_headers': context.get('request_headers'),
                            'request_body': context.get('request_body'),
                            'response_headers': context.get('response_headers'),
                            'response_body': context.get('response_body')
                        }
                    }
                else:
                    result = {
                        'violation_type': violation_type,
                        'username': username,
                        'resource_url': url,
                        'details': 'No violation of the least privilege principle detected.'  # Changed to English
                    }

            # Create the final result
            final_result = {
                'vulnerability_type': violation_type,
                'vulnerability_name': 'Least Privilege Violation',
                'description': json.dumps(result, indent=2, ensure_ascii=False),
                'additional_info': {  # Include security recommendations
                    'recommendations': [  # Changed to English
                        'Check the authentication and authorization configuration.',
                        'Ensure that sensitive resources are only accessible to authenticated users.',
                        'Implement the principle of least privilege to restrict access to resources.'
                    ]
                }
            }

            # Store in context['results'] as a list
            context['results'] = [final_result]

            return context

        except Exception as e:
            context.setdefault('errors', []).append(f"Error in ReportViolationLeastPriv : {e}")  # Changed to English
            return context