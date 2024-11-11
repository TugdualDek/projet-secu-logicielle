import re
from backend.kernel.module_loader import load_modules
from backend.kernel.workflow_parser import load_workflow, get_all_workflows

class Kernel:
    def __init__(self):
        self.modules = load_modules()

    def execute_all_workflows(self, context):
        workflows = get_all_workflows()
        combined_results = {}

        for workflow_name in workflows:
            print(f"Exécution du workflow: {workflow_name}")
            workflow_context = context.copy()
            workflow_results = self.execute_workflow(workflow_name, workflow_context)
        
            # Ajouter les résultats du workflow au contexte global
            combined_results[workflow_name] = workflow_results

        print(f"Résultats combinés de tous les workflows: {combined_results}")
        # Retourner les résultats combinés de tous les workflows
        return combined_results

    def execute_workflow(self, workflow_name, context):
        workflow = load_workflow(workflow_name)
        pattern = re.compile(r'\{\{\s*(\w+)\s*\}\}')

        for step in workflow.get('steps', []):
            module_name = step['module']
            params = step.get('params', {})

            # Fusionner les paramètres statiques avec les paramètres du contexte
            merged_params = {**params}

            # Substituer les variables dans les paramètres fusionnés
            substituted_params = {}
            for key, value in merged_params.items():
                if isinstance(value, str):
                    # Trouver toutes les variables dans la forme {{variable}}
                    matches = pattern.findall(value)
                    for var in matches:
                        if var in context:
                            # Remplacer {{variable}} par sa valeur dans le contexte
                            value = re.sub(r'\{\{\s*' + var + r'\s*\}\}', str(context[var]), value)
                        else:
                            raise Exception(f"Variable {var} non trouvée dans le contexte")
                substituted_params[key] = value

            # Mettre à jour le contexte avec les paramètres substitués
            context.update(substituted_params)

            print(f"Exécution du module: {module_name}")
            print(f"Contexte: {context}")

            module = self.modules.get(module_name)
            if module:
                # Exécuter le module et mettre à jour le contexte
                context = module.run(context)
            else:
                raise Exception(f"Module {module_name} non trouvé")

            print(f"Contexte après exécution: {context}")

        # Retourner les résultats finaux du workflow
        return context.get('results', {})