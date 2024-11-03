from abc import ABC, abstractmethod
from typing import Dict, Any, List


class BaseScanner(ABC):
    """Classe de base pour tous les scanners"""

    def __init__(self, target: str):
        """
        Initialise le scanner avec une cible et des paramètres initiaux.
        
        :param target: La cible à scanner.
        """
        self.target = target  # La cible à scanner
        self.results = []  # Les résultats du scan
        self.status = "ready"  # Le statut du scanner: "ready", "running", "completed", "error"

    @abstractmethod
    def scan(self) -> Dict[str, Any]:
        """
        Méthode abstraite que chaque scanner doit implémenter.
        
        :return: Un dictionnaire contenant les résultats du scan.
        """
        pass

    def add_result(self, result: Dict[str, Any]):
        """
        Ajoute un résultat au scanner.
        
        :param result: Un dictionnaire contenant le résultat du scan.
        """
        self.results.append(result)

    def get_results(self) -> List[Dict[str, Any]]:
        """
        Retourne tous les résultats du scan.
        
        :return: Une liste de dictionnaires contenant les résultats du scan.
        """
        return self.results
