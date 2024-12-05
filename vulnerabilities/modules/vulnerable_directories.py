import requests
import urllib.parse
from bs4 import BeautifulSoup

class InformationLeakScanner:
    @staticmethod
    def detect_directory_listing(base_url):

        try:
            response = requests.get(base_url, allow_redirects=False)
            if 'Index of' in response.text or 'directory listing' in response.text.lower():
                print(f"⚠️ Liste de répertoires potentiellement exposée : {base_url}")

                # Extraction des liens
                soup = BeautifulSoup(response.text, 'html.parser')
                links = soup.find_all('a')
                for link in links:
                    href = link.get('href')
                    if href and not href.startswith('/'):
                        print(f"  Fichier potentiellement exposé : {urllib.parse.urljoin(base_url, href)}")

        except requests.exceptions.RequestException as e:
            print(f"Erreur de requête : {e}")

