from abc import ABC

import requests
from typing import List, Dict, Any
from ..common.base_scanner import BaseScanner
import time

class BruteforceScanner(BaseScanner, ABC):
    """Scanner pour attaques par force brute"""

    def __init__(self, target: str, usernames: List[str] = None, passwords: List[str] = None):
        super().__init__(target)
        self.usernames = usernames or ['admin', 'root', 'user', 'test']
        self.passwords = passwords or self._load_common_passwords()
        self.successful_attempts = []

    def _load_common_passwords(self) -> List[str] :
        """Charge une liste de mdp communs"""
        return [
            '123456', 'password', 'admin', 'admin123',
            'root', '12345', 'toor', 'test123'
        ]

    def scan(self) -> Dict[str, Any]:
        """Exécute le scan """
        self.status = "running"
        start_time = time.time()

        try:
            for username in self.usernames:
                for password in self.passwords:
                    result = self._try_login(username, password)
                    if result:
                        self.successful_attempts.append({
                            'username': username,
                            'password': password
                        })
            end_time = time.time()
            duration = end_time - start_time

            scan_result = {
                'vulnerability_type': 'bruteforce',
                'target': self.target,
                'successful_attempts': self.successful_attempts,
                'total_attempts': len(self.usernames) * len(self.passwords),
                'duration': duration,
                'status': 'completed' if len(self.successful_attempts) > 0 else 'failed',
                'severity': 'high' if len(self.successful_attempts) > 0 else 'low'
            }

            self.add_result(scan_result)
            self.status = "completed"
            return scan_result

        except Exception as e:
            self.status = "error"
            return {
                'vulnerability_type': 'bruteforce',
                'target': self.target,
                'error': str(e),
                'status': 'error'
            }
            self.add_result(error_result)
            self.status = "error"
            return error_result

    def _try_login(self, username: str, password: str) -> Dict[str, Any]:
        """Tente une connexion avec un nom d'utilisateur et un mot de passe'"""
        try:
            response = request.post(
                f"{self.target}/auth/login",
                json={
                    "email": username,
                    "password": password
                },
                timeout=5
            )

            sucess = response.status_code == 200

            return {
                'sucess': sucess,
                'status_code': response.status_code,
                'response':response.json() if sucess else None
            }

        except requests.exceptions.RequestException:
            return {
                'sucess': False,
                'status_code': None,
                'error':'connection failed'
            }
