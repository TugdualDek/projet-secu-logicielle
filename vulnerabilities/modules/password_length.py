import re
import requests

class PasswordSecurity:
    def __init__(self, url):
        self.url = url
        self.session = requests.Session()
        self.vulnerabilities = []

    def check_password_length(self, min_length=8):

        try:

            short_password = 'a' * (min_length - 1)
            long_password = 'a' * min_length


            data_short = {
                'username': 'test_user_short',
                'password': short_password
            }
            response_short = self.session.post(f'{self.url}/register', json=data_short)

            if response_short.status_code == 200:
                self.vulnerabilities.append(f"Mot de passe trop court accepté : {len(short_password)} caractères")

            # Vérification validation côté client
            response = self.session.get(f'{self.url}/register')
            client_side_validation = self._check_client_side_validation(response.text)

            if not client_side_validation:
                self.vulnerabilities.append("Pas de validation côté client pour la longueur du mot de passe")

        except Exception as e:
            self.vulnerabilities.append(f"Erreur vérification longueur : {e}")

    def _check_client_side_validation(self, html_content):

        validation_patterns = [
            r'minlength=["\'](\d+)["\']',
            r'pattern=["\'](.+?)["\']',
            r'required'
        ]

        for pattern in validation_patterns:
            if re.search(pattern, html_content, re.IGNORECASE):
                return True
        return False

    def check_password_complexity(self):
        complexity_checks = [
            r'[A-Z]',  # Majuscule
            r'[a-z]',  # Minuscule
            r'\d',  # Chiffre
            r'[!@#$%^&*()]'  # Caractère spécial
        ]

        simple_password = 'password123'

        try:
            data = {
                'username': 'test_user_simple',
                'password': simple_password
            }
            response = self.session.post(f'{self.url}/register', json=data)

            if response.status_code == 200:
                # Vérifier si le mot de passe respecte tous les critères
                failed_checks = [check for check in complexity_checks if not re.search(check, simple_password)]

                if failed_checks:
                    self.vulnerabilities.append("Politique de mot de passe faible")
        except Exception as e:
            self.vulnerabilities.append(f"Erreur vérification complexité : {e}")

    def scan(self):
        self.check_password_length()
        self.check_password_complexity()

        return {
            "url": self.url,
            "vulnerabilities": self.vulnerabilities,
            "secure": len(self.vulnerabilities) == 0
        }


# Exemple
scanner = PasswordSecurity('https://moodle.isep.fr/moodle/login/index.php?authCAS=CAS')
resultats = scanner.scan()
print(resultats)