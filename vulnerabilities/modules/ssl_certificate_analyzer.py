from vulnerabilities.modules.base_module import BaseModule
import ssl
import socket
from datetime import datetime

class Module(BaseModule):
    def run(self, context):
        url = context.get('target', '')
        module_results = context.setdefault('module_results', [])
        
        if not url:
            module_results.append({
                'TLS Analysis': {
                    'error': 'No URL provided for analysis'
                }
            })
            return context

        hostname = url.split('://')[1].split('/')[0]
        
        try:
            context_ssl = ssl.create_default_context()
            with socket.create_connection((hostname, 443)) as sock:
                with context_ssl.wrap_socket(sock, server_hostname=hostname) as ssock:
                    cert = ssock.getpeercert()
                    
                    # Analyse TLS
                    tls_version = ssock.version()
                    cipher = ssock.cipher()
                    
                    # Dates du certificat
                    not_before = datetime.strptime(cert['notBefore'], '%b %d %H:%M:%S %Y GMT')
                    not_after = datetime.strptime(cert['notAfter'], '%b %d %H:%M:%S %Y GMT')
                    
                    # Analyse des vulnérabilités
                    vulnerabilities = []
                    is_vulnerable = False
                    
                    # Vérification TLS
                    if tls_version in ['TLSv1', 'TLSv1.1']:
                        vulnerabilities.append(f"Obsolete TLS version detected: {tls_version}")
                        is_vulnerable = True
                    
                    # Vérification cipher
                    weak_ciphers = ['RC4', 'DES', '3DES', 'MD5']
                    if any(weak in cipher[0] for weak in weak_ciphers):
                        vulnerabilities.append(f"Weak cipher detected: {cipher[0]}")
                        is_vulnerable = True
                    
                    # Vérification validité certificat
                    current_time = datetime.utcnow()
                    if current_time > not_after:
                        vulnerabilities.append("Certificate has expired")
                        is_vulnerable = True
                    if current_time < not_before:
                        vulnerabilities.append("Certificate not yet valid")
                        is_vulnerable = True

                    module_results.append({
                        'TLS Analysis': {
                            'vulnerable': is_vulnerable,
                            'tls_version': tls_version,
                            'cipher_suite': {
                                'name': cipher[0],
                                'protocol': cipher[1],
                                'bits': cipher[2]
                            },
                            'certificate_info': {
                                'subject': dict(cert['subject'][0]),
                                'issuer': dict(cert['issuer'][0]),
                                'valid_from': not_before.strftime('%Y-%m-%d %H:%M:%S GMT'),
                                'valid_until': not_after.strftime('%Y-%m-%d %H:%M:%S GMT'),
                                'san': cert.get('subjectAltName', []),
                                'ocsp': cert.get('OCSP', []),
                                'caIssuers': cert.get('caIssuers', [])
                            },
                            'vulnerabilities': vulnerabilities if vulnerabilities else "No TLS vulnerabilities detected",
                            'validation_status': {
                                'is_expired': current_time > not_after,
                                'is_not_yet_valid': current_time < not_before,
                                'is_valid': not_before <= current_time <= not_after
                            }
                        }
                    })
                    
        except ssl.SSLError as e:
            module_results.append({
                'TLS Analysis': {
                    'error': f'SSL Error: {str(e)}',
                    'vulnerable': True
                }
            })
        except socket.error as e:
            module_results.append({
                'TLS Analysis': {
                    'error': f'Connection Error: {str(e)}',
                    'vulnerable': True
                }
            })
        except Exception as e:
            module_results.append({
                'TLS Analysis': {
                    'error': f'Error during TLS analysis: {str(e)}',
                    'vulnerable': True
                }
            })
            
        return context
