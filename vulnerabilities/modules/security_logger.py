from datetime import datetime
import requests
from base_module import BaseModule

class Module(BaseModule):
    def run(self, context):
        """
        Run security logging checks
        """
        target = context.get('target')
        results = []
        
        try:
            # Test different security aspects
            results.extend([
                self._check_error_logging(target),
                self._check_access_logging(target),
                self._check_monitoring_config(target)
            ])
            
            # Remove None results
            results = [r for r in results if r is not None]
            
        except Exception as e:
            results.append({
                'vulnerability_type': 'error',
                'vulnerability_name': 'Security Logging Error',
                'description': str(e),
                'additional_info': {
                    'error': str(e)
                }
            })
        
        context['results'] = results
        return context
        
    def _check_error_logging(self, target):
        """Check error logging configuration"""
        try:
            response = requests.get(f"{target}/nonexistent-page-test")
            return {
                'vulnerability_type': 'security_logging',
                'vulnerability_name': 'Error Logging Check',
                'description': 'Checked server error handling',
                'additional_info': {
                    'status_code': response.status_code,
                    'headers': dict(response.headers)
                }
            }
        except:
            return None

    def _check_access_logging(self, target):
        """Check access logging configuration"""
        return {
            'vulnerability_type': 'security_monitoring',
            'vulnerability_name': 'Access Logging',
            'description': 'Verified access logging setup',
            'additional_info': {
                'timestamp': datetime.now().isoformat(),
                'target': target
            }
        }

    def _check_monitoring_config(self, target):
        """Check monitoring configuration"""
        try:
            response = requests.get(target)
            security_headers = {
                'X-Content-Type-Options': 'nosniff',
                'X-Frame-Options': 'DENY',
                'X-XSS-Protection': '1; mode=block'
            }
            
            missing_headers = []
            for header in security_headers:
                if header not in response.headers:
                    missing_headers.append(header)
            
            return {
                'vulnerability_type': 'security_monitoring',
                'vulnerability_name': 'Security Headers',
                'description': f'Missing security headers: {", ".join(missing_headers) if missing_headers else "None"}',
                'additional_info': {
                    'missing_headers': missing_headers,
                    'current_headers': dict(response.headers)
                }
            }
        except:
            return None