from base_module import BaseModule
import json

class Module(BaseModule):
  def run(self, context):
    try:
        # Récupérer l'URL du contexte
        vulnerable_url = context.get('target')

        # Vérifier si l'URL est présente dans le contexte
        if not vulnerable_url:
            raise ValueError("URL manquante dans le contexte pour signaler la violation CSRF.")

        # Récupérer les informations du contexte
        violation_type = context.get('violation_type', 'csrf')
        details = context.get('details', '')
        request_status = context.get('request_status')
        response_content = context.get('response_content')
        attack_value = context.get('attack_value')

        # Créer le dictionnaire de résultats
        result = {}

        if request_status == 200 and attack_value in response_content:
            result = {
                'vulnerability_type': violation_type,
                'vulnerable_url': vulnerable_url
            }
            if details:
                result['details'] = details
        else:
            result = {
                'vulnerability_type': violation_type,
                'vulnerable_url': vulnerable_url,
                'details': 'Aucune vulnérabilité détectée.'
            }

        # Créer le résultat final
        final_result = {
            'vulnerability_type': violation_type,
            'vulnerability_name': 'CSRF Vulnerability',
            'description': json.dumps(result, indent=2, ensure_ascii=False),
            'additional_info': None
        }

        # Stocker dans context['results'] sous forme de liste
        context['results'] = [final_result]

        return context

    except Exception as e:
        context.setdefault('errors', []).append(f"Erreur dans report_violation_csrf : {e}")
        return context
