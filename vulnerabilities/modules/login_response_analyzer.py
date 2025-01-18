from vulnerabilities.modules.base_module import BaseModule

class LoginResponseAnalyzer:
    """
    Analyse la réponse HTTP et décide si la connexion est réussie
    (score ou booléen).
    """
    def is_login_success(self, response, context):
        """
        Retourne True ou False selon la logique de scoring.
        """
        raise NotImplementedError("is_login_success() must be implemented.")


class DefaultLoginResponseAnalyzer(LoginResponseAnalyzer):
    def __init__(self):
        self.baseline_response = None
        self.baseline_length = None

    def is_login_success(self, response, context):
        """
        Détecte le succès de connexion en comparant avec une baseline
        """
        # Première requête = baseline (échec connu)
        if not self.baseline_response:
            self.baseline_response = response.text
            self.baseline_length = len(response.text)
            return False

        current_length = len(response.text)

        # Si la réponse est très différente de la baseline
        if abs(current_length - self.baseline_length) > (self.baseline_length * 0.3):
            return True

        # Si le formulaire de login n'est plus présent
        if '<form' in self.baseline_response and '<form' not in response.text:
            return True

        # Si de nouveaux liens/boutons apparaissent
        baseline_links = self.baseline_response.count('<a href')
        current_links = response.text.count('<a href')
        if current_links > (baseline_links * 1.5):
            return True

        return False


class Module(BaseModule):
    def __init__(self):
        self.analyzer = DefaultLoginResponseAnalyzer()

    def run(self, context):
        """
        Analyse la réponse de connexion et met à jour le contexte avec le résultat.
        """
        response = context.get('response')
        if not response:
            context.setdefault('errors', []).append("Aucune réponse à analyser")
            return context

        success = self.analyzer.is_login_success(response, context)
        context['login_result'] = {
            'success': success,
            'score_threshold': 60,  # Correspond au seuil défini dans DefaultLoginResponseAnalyzer
            'response_code': response.status_code
        }

        return context