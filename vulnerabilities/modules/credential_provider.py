from abc import ABC, abstractmethod
from urllib.parse import urlparse
import datetime
from vulnerabilities.modules.base_module import BaseModule

class CredentialProvider(ABC):
    """
    Classe responsable de fournir une liste de paires (username, password).
    On peut imaginer plusieurs providers : dictionnaire, génération dynamique, etc.
    """
    @abstractmethod
    def get_credentials(self, context):
        """
        Retourne un itérable de tuples (username, password).
        :param context: Dictionnaire contenant, par exemple, le 'target_url' etc.
        """
        pass


class CommonCredentialsStrategy:
    """
    Stratégie pour générer des crédentiels courants.
    """
    def __init__(self, usernames, passwords):
        self.usernames = usernames
        self.passwords = passwords

    def generate(self, context):
        for u in self.usernames:
            for p in self.passwords:
                yield u, p


class ContextualCredentialsStrategy:
    """
    Stratégie pour générer des crédentiels basés sur le contexte (ex: domaine, année).
    """
    def generate(self, context):
        url = context.get('target') or context.get('url')
        if not url:
            return  # Aucun URL cible fourni

        parsed_url = urlparse(url)
        domain = parsed_url.netloc
        year = datetime.datetime.now().year

        # Exemples de crédentiels contextuels
        yield f"admin@{domain}", "admin123"
        yield f"root@{domain}", f"{domain}{year}"
        yield f"support@{domain}", f"support{year}"
        yield f"user@{domain}", f"user{year}!"


class DictionaryCredentialsStrategy:
    """
    Stratégie pour générer des crédentiels à partir d'un dictionnaire externe.
    """
    def __init__(self, dictionary_path):
        self.dictionary_path = dictionary_path

    def generate(self, context):
        try:
            with open(self.dictionary_path, 'r', encoding='utf-8') as file:
                for line in file:
                    line = line.strip()
                    if not line or ':' not in line:
                        continue  # Ignorer les lignes invalides
                    username, password = line.split(':', 1)
                    yield username.strip(), password.strip()
        except FileNotFoundError:
            # Gérer le cas où le fichier n'existe pas
            pass


class DefaultCredentialProvider(CredentialProvider):
    def __init__(self, config=None):
        self.config = config or {}
        self.strategies = []
        self._init_strategies()

    def _init_strategies(self):
        c = self.config.get('credential_provider', {})
        common_usernames = c.get('common_usernames', ["admin", "test", "user"])
        common_passwords = c.get('common_passwords', ["admin123", "Pass123!", "password"])

        # Stratégie "commune"
        if common_usernames and common_passwords:
            self.strategies.append(CommonCredentialsStrategy(common_usernames, common_passwords))

        # Stratégie "contextuelle"
        self.strategies.append(ContextualCredentialsStrategy())

        # Stratégie "dictionnaire" (optionnelle)
        dictionary_path = c.get('dictionary_path')
        if dictionary_path:
            self.strategies.append(DictionaryCredentialsStrategy(dictionary_path))

    def get_credentials(self, context):
        """
        Génère les crédentiels en combinant toutes les stratégies,
        + ceux spécifiés directement dans le contexte (usernames/passwords).
        """
        # 1. Si le YAML a défini "usernames" et "passwords", on les injecte via CommonCredentialsStrategy
        if 'usernames' in context and 'passwords' in context:
            dynamic_usernames = context['usernames']
            dynamic_passwords = context['passwords']

            yield from CommonCredentialsStrategy(dynamic_usernames, dynamic_passwords).generate(context)

        # 2. Ensuite, on yield le reste (stratégies par défaut ou config)
        for strategy in self.strategies:
            yield from strategy.generate(context)


class Module(BaseModule):
    def __init__(self):
        self.provider = DefaultCredentialProvider()

    def run(self, context):
        """
        Génère les identifiants et les stocke dans le contexte.
        """
        try:
            credentials = list(self.provider.get_credentials(context))
            context['generated_credentials'] = credentials
            context['credentials_count'] = len(credentials)
        except Exception as e:
            context.setdefault('errors', []).append(f"Erreur lors de la génération des identifiants : {str(e)}")

        return context