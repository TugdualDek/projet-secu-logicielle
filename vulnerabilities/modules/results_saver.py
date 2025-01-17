from vulnerabilities.modules.base_module import BaseModule
import json

class Module(BaseModule):
    def run(self, context):
        vulnerability_type = context.get('vulnerability_type', 'Unknown')
        vulnerability_name = context.get('vulnerability_name', 'Unknown')
        module_results = context.get('module_results', [])

        # Sérialiser les résultats importants des modules en JSON
        description = json.dumps(module_results, indent=2, ensure_ascii=False)

        # Créer le résultat final
        final_result = {
            'vulnerability_type': vulnerability_type,
            'vulnerability_name': vulnerability_name,
            'description': description,
            'additional_info': None  # Ajouter des informations supplémentaires si nécessaire
        }

        # Stocker dans context['results'] sous forme de liste
        context['results'] = [final_result]

        return context
