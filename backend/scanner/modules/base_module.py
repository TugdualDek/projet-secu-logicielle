from abc import ABC, abstractmethod

class BaseModule(ABC):
    @abstractmethod
    def run(self, context):
        """
        Méthode principale que chaque module doit implémenter.
        :param context: Dictionnaire contenant le contexte d'exécution.
        """
        pass
