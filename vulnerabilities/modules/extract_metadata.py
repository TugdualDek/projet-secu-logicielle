from abc import abstractmethod
import requests
from bs4 import BeautifulSoup
from base_module import BaseModule

class Module(BaseModule):

    @abstractmethod
    def extract_metadata(self, url):
        try:
            response = requests.get(url)

            headers = response.headers
            print("En-têtes potentiellement sensibles :")
            for key, value in headers.items():
                if key.lower() in ['server', 'x-powered-by', 'via']:
                    print(f" {key}: {value}")

            soup = BeautifulSoup(response.text, 'html.parser')

            comments = soup.find_all(text=lambda text: isinstance(text, str) and '<!--' in text)
            for comment in comments:
                print(f" Commentaire sensible trouvé : {comment}")

            scripts = soup.find_all('script')
            for script in scripts:
                if script.string and ('config' in script.string.lower() or 'credentials' in script.string.lower()):
                    print(" Script potentiellement sensible détecté")

        except requests.exceptions.RequestException as e:
            print(f"Erreur de requête : {e}")
