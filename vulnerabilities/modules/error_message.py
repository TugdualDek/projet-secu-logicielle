import requests
import re

class InformationLeakScanner:
    @staticmethod
    def scan_error_messages(url):
        sensitive_patterns = [
            r'database error',
            r'SQL syntax',
            r'stack trace',
            r'internal server error',
            r'debug information'
        ]

        try:
            response = requests.get(url)
            for pattern in sensitive_patterns:
                if re.search(pattern, response.text, re.IGNORECASE):
                    print(f" Fuite potentielle : {pattern} détecté")
        except requests.exceptions.RequestException as e:
            print(f"Erreur de requête : {e}")
