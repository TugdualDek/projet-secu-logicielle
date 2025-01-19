from base_module import BaseModule
import json

class Module(BaseModule):
    def run(self, context):
        try:
            # Récupérer les informations du contexte
            violation_type = context.get('violation_type', 'least_privilege')
            username = context.get('username')
            url = context.get('target')
            if not url:
                raise ValueError("URL manquante dans le contexte pour envoyer la requête malveillante.")
            access_result = context.get('access_result')
            error_code = context.get('error_code')  # Récupérer le code d’erreur

            if not all([username, url, access_result]):
                print("Informations manquantes dans le contexte pour générer le rapport.")

            # Créer le dictionnaire de résultats
            result = {}

            if error_code:  # Vérifier si un code d'erreur est présent
                result = {
                    'violation_type': violation_type,
                    'username': username,
                    'resource_url': url,
                    'details': 'Erreur lors de la vérification du moindre privilège.',
                    'error_code': error_code
                }
            elif access_result:  # Si pas d'erreur et accès autorisé
                result = {
                    'violation_type': violation_type,
                    'username': username,
                    'resource_url': url,
                    'details': 'Violation du principe du moindre privilège détectée !'
                }
            else:  # Si pas d'erreur et accès refusé
                if any("Erreur de connexion" in err for err in context.get('errors', [])):
                    result = {
                        'violation_type': violation_type,
                        'username': username,
                        'resource_url': url,
                        'details': 'Vulnérabilité potentielle : Accès autorisé malgré une erreur de connexion.'
                    }
                else:
                    result = {
                        'violation_type': violation_type,
                        'username': username,
                        'resource_url': url,
                        'details': 'Aucune violation du principe du moindre privilège détectée.'
                    }

            # Créer le résultat final
            final_result = {
                'vulnerability_type': violation_type,
                'vulnerability_name': 'Least Privilege Violation',
                'description': json.dumps(result, indent=2, ensure_ascii=False),
                'additional_info': None
            }
            print(final_result)
            
            # Stocker dans context['results'] sous forme de liste
            context['results'] = [final_result]

            return context

        except Exception as e:
            context.setdefault('errors', []).append(f"Erreur dans ReportViolationLeastPriv : {e}")
            return context
