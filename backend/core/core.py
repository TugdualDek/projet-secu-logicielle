import re
from backend.core.module_loader import load_modules
from backend.core.workflow_parser import load_workflow, get_all_workflows
from backend.tasks import save_results_callback

def substitute_variables(value, context, pattern):
    """
    substitute_variables Substitue les variables dans une valeur donnée en utilisant le contexte fourni.
    :param value: Valeur à traiter
    :param context: Contexte contenant les variables
    :param pattern: Expression régulière pour identifier les variables
    :return: Valeur avec les variables substituées
    """
    if isinstance(value, str):
        matches = pattern.findall(value)
        for var in matches:
            # Gérer les clés imbriquées
            keys = var.split('.')
            temp = context
            for key in keys:
                if key in temp:
                    temp = temp[key]
                else:
                    raise Exception(f"Variable {var} non trouvée dans le contexte")
            value = re.sub(r'\{\{\s*' + var + r'\s*\}\}', str(temp), value)
        return value
    elif isinstance(value, list):
        return [substitute_variables(item, context, pattern) for item in value]
    elif isinstance(value, dict):
        return {k: substitute_variables(v, context, pattern) for k, v in value.items()}
    else:
        # Pour les autres types (int, float, bool, etc.), on retourne la valeur telle quelle
        return value

class Core:
    def __init__(self):
        self.modules = None

    def load_modules(self):
        """
        load_modules Charge les modules disponibles
        """
        if self.modules is None:
            self.modules = load_modules()

    def execute_all_workflows(self, context):
        """
        :param context: Contexte initial
        :return: Résultats combinés de tous les workflows
        """
        self.load_modules()
        workflows = get_all_workflows()

        for workflow_name in workflows:
            print(f"Exécution du workflow: {workflow_name}")
            workflow_context = context.copy()
            workflow_results = self.execute_workflow(workflow_name, workflow_context)

            # Enregistrer les résultats du workflow actuel
            save_results_callback(workflow_name, workflow_results)

            # Nettoyer le contexte tout en conservant les données partagées
            context = self.clean_context(workflow_context, context)
            
        self.modules = None

    def execute_workflow(self, workflow_name, context):
        """
        execute_workflow Exécute un workflow donné
        :param workflow_name: Nom du workflow
        :param context: Contexte initial
        :return: Résultats du workflow
        """
        workflow = load_workflow(workflow_name)
        pattern = re.compile(r'\{\{\s*(\w+)\s*\}\}')

        for step in workflow.get('steps', []):
            module_name = step['module']
            params = step.get('params', {})

            # Fusionner les paramètres statiques avec les paramètres du contexte
            merged_params = {**params}

            # Substituer les variables dans les paramètres fusionnés
            substituted_params = substitute_variables(merged_params, context, pattern)

            # Mettre à jour le contexte avec les paramètres substitués
            context.update(substituted_params)

            print(f"Exécution du module: {module_name}")
            print(f"Contexte: {context}")

            module = self.modules.get(module_name)
            if module:
                context = module.run(context)
            else:
                raise Exception(f"Module {module_name} non trouvé")

            print(f"Contexte après exécution: {context}")

        return context.get('results', {})
    
    def clean_context(self, workflow_context, shared_context):
        """
        Nettoie le contexte en conservant les données partagées.
        """
        # Certaines clés ne doivent pas être supprimées du contexte
        shared_keys = ['target', 'scan_id', 'shared_data']
        new_context = {key: shared_context[key] for key in shared_keys if key in shared_context}
        return new_context