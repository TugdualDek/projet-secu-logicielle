import requests
import socket
import ssl

class TransportVulnerabilityScanner:

    @staticmethod
    def analyze_ssl_configuration(hostname, port=443):
        """
        Analyse la configuration SSL/TLS
        """
        try:
            context = ssl.create_default_context()
            with socket.create_connection((hostname, port)) as sock:
                with context.wrap_socket(sock, server_hostname=hostname) as secure_sock:
                    cert = secure_sock.getpeercert(binary_form=False)

                    # Vérification de l'expiration du certificat
                    import datetime
                    expiry = datetime.datetime.strptime(cert['notAfter'], '%b %d %H:%M:%S %Y %Z')
                    if expiry < datetime.datetime.now():
                        print("⚠️ Certificat SSL expiré")

                    # Vérification des protocoles faibles
                    protocols = secure_sock.version()
                    weak_protocols = ['SSLv2', 'SSLv3', 'TLSv1.0']
                    if any(proto in protocols for proto in weak_protocols):
                        print(f"⚠️ Protocole faible détecté : {protocols}")

        except ssl.SSLError as e:
            print(f"Erreur SSL : {e}")
