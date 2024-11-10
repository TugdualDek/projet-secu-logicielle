import re
from backend.kernel.module_loader import load_modules
from backend.kernel.workflow_parser import load_workflow, get_all_workflows

class Kernel:
    def __init__(self):
        self.modules = load_modules()

    def execute_all_workflows(self, context):
        workflows = get_all_workflows()
        for workflow_name in workflows:
            print(f"Exécution du workflow: {workflow_name}")
            workflow_context = context.copy()
            self.execute_workflow(workflow_name, workflow_context)

    def execute_workflow(self, workflow_name, context):
        workflow = load_workflow(workflow_name)
        pattern = re.compile(r'\$\{(\w+)\}')

        for step in workflow:
            module_name = step['module']
            params = step.get('params', {})

            # Substituer les variables dans les paramètres
            substituted_params = {}
            for key, value in params.items():
                if isinstance(value, str):
                    # Trouver toutes les variables dans la forme ${variable}
                    matches = pattern.findall(value)
                    for var in matches:
                        if var in context:
                            # Remplacer ${variable} par sa valeur dans le contexte
                            value = value.replace(f"${{{var}}}", str(context[var]))
                        else:
                            raise Exception(f"Variable {var} non trouvée dans le contexte")
                substituted_params[key] = value

            # Mettre à jour le contexte avec les paramètres substitués
            context.update(substituted_params)

            module = self.modules.get(module_name)
            if module:
                context = module.run(context)
            else:
                raise Exception(f"Module {module_name} non trouvé")
        return context