import re
from abc import abstractmethod
from base_module import BaseModule

class Module(BaseModule):
    @abstractmethod
    def check_password_complexity(self, password):
        if len(password) < 12:
            print("Mot de passe trop court")
            return False
        criteria = [
            r'[A-Z]',
            r'[a-z]',
            r'[0-9]',
            r'[!@#$%^&*(),.?":{}|<>]'
        ]
        passed_criteria = sum(1 for criterion in criteria if re.search(criterion, password))
        if passed_criteria < 3:
            print("Mot de passe pas assez complexe")
            return False
        return True
