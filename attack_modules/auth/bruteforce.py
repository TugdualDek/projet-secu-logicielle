from abc import ABC
import requests
from typing import List, Dict, Any
from ..common.base_scanner import BaseScanner
import time

class BruteforceScanner(BaseScanner, ABC):
    def __init__(self, target: str, usernames: List[str] = None, passwords: List[str] = None):
        super().__init__(target)
        self.usernames = usernames or [
            'admin@test.com',
            'test@test.com',
            'said@gmail.com',
            'hello@gmail.com',
        ]
        self.passwords = passwords or self._load_common_passwords()
        self.successful_attempts = []

    @staticmethod
    def _load_common_passwords() -> List[str]:
        """Charge une liste de mots de passe couramment utilisés"""
        return [
            '123456', 'password', '12345', '2f15'
        ]

    def scan(self) -> Dict[str, Any]:
        """Exécute le scan avec un délai entre chaque tentative"""
        self.status = "running"
        start_time = time.time()
        total_attempts = 0

        try:
            for username in self.usernames:
                for password in self.passwords:
                    # Ajouter un délai de 1 seconde entre chaque tentative
                    time.sleep(0.01)
                    total_attempts += 0.01
                    print(f"Tentative {total_attempts}: {username} / {password}")  # Log pour suivre la progression

                    result = self._try_login(username, password)
                    if result.get('success'):
                        self.successful_attempts.append({
                            'username': username,
                            'password': password
                        })
                        print(f"Succès trouvé! Email: {username}, Password: {password}")
                        # Option: arrêter après le premier succès
                        # return self._create_result(start_time, total_attempts)

            return self._create_result(start_time, total_attempts)

        except Exception as e:
            error_result = {
                'vulnerability_type': 'bruteforce',
                'target': self.target,
                'error': str(e),
                'status': 'error',
                'total_attempts': total_attempts
            }
            self.add_result(error_result)
            self.status = "error"
            return error_result

    def _create_result(self, start_time: float, total_attempts: int) -> Dict[str, Any]:
        """Crée le rapport de résultats"""
        end_time = time.time()
        duration = end_time - start_time

        return {
            'vulnerability_type': 'bruteforce',
            'target': self.target,
            'successful_attempts': self.successful_attempts,
            'total_attempts': total_attempts,
            'duration': duration,
            'status': 'completed' if self.successful_attempts else 'failed',
            'severity': 'high' if self.successful_attempts else 'low'
        }

    def _try_login(self, username: str, password: str) -> Dict[str, Any]:
        """Tente une connexion avec un email et un mot de passe"""
        try:
            response = requests.post(
                self.target,
                json={
                    "email": username,
                    "password": password
                },
                timeout=5
            )

            success = response.status_code == 200

            return {
                'success': success,
                'status_code': response.status_code,
                'response': response.json() if success else None
            }

        except requests.exceptions.RequestException as e:
            return {
                'success': False,
                'status_code': None,
                'error': f'Connection failed: {str(e)}'
            }