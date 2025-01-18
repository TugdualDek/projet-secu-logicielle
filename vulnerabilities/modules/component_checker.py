from base_module import BaseModule
import requests
from bs4 import BeautifulSoup

class Module(BaseModule):
    def run(self, context):
        """
        Run component version checks
        """
        target = context.get('target')
        results = []
        
        try:
            response = requests.get(target)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Check frameworks
            frameworks = self._detect_frameworks(soup, response)
            for framework, version in frameworks.items():
                results.append({
                    'vulnerability_type': 'outdated_component',
                    'vulnerability_name': f'Framework: {framework}',
                    'description': f'Detected version: {version}',
                    'additional_info': {
                        'component_type': 'framework',
                        'name': framework,
                        'version': version
                    }
                })
            
            # Check libraries
            libraries = self._detect_libraries(soup)
            for library in libraries:
                results.append({
                    'vulnerability_type': 'component_check',
                    'vulnerability_name': f'Library: {library}',
                    'description': 'Library detected in use',
                    'additional_info': {
                        'component_type': 'library',
                        'name': library
                    }
                })
            
            # Check server technology
            server = response.headers.get('Server')
            if server:
                results.append({
                    'vulnerability_type': 'server_technology',
                    'vulnerability_name': f'Server: {server}',
                    'description': 'Server technology detected',
                    'additional_info': {
                        'component_type': 'server',
                        'name': server
                    }
                })

        except Exception as e:
            results.append({
                'vulnerability_type': 'error',
                'vulnerability_name': 'Component Check Error',
                'description': str(e),
                'additional_info': {
                    'error': str(e)
                }
            })

        context['results'] = results
        return context

    def _detect_frameworks(self, soup, response):
        """Detect frameworks and their versions"""
        frameworks = {}
        
        # Check headers
        if 'X-Powered-By' in response.headers:
            frameworks['Server-Side'] = response.headers['X-Powered-By']
            
        # Check common framework signatures
        if soup.select('[ng-app]'):
            frameworks['Angular'] = 'Version Unknown'
        if soup.select('[data-reactroot]'):
            frameworks['React'] = 'Version Unknown'
        if soup.select('[data-vue]'):
            frameworks['Vue.js'] = 'Version Unknown'
            
        return frameworks

    def _detect_libraries(self, soup):
        """Detect JavaScript libraries"""
        libraries = set()
        
        for script in soup.find_all('script'):
            src = script.get('src', '').lower()
            
            # Check common libraries
            if 'jquery' in src:
                libraries.add('jQuery')
            if 'bootstrap' in src:
                libraries.add('Bootstrap')
            if 'lodash' in src:
                libraries.add('Lodash')
            
        return list(libraries)