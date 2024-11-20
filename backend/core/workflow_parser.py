import yaml
import os

WORKFLOWS_DIR = "vulnerabilities/workflows"

def load_workflow(workflow_name):
    """
    load_workflow Charge un workflow à partir d'un fichier YAML
    :param workflow_name: Nom du workflow
    :return: Workflow
    """
    workflow_file = os.path.join(WORKFLOWS_DIR, f"{workflow_name}.yaml")
    with open(workflow_file, 'r') as f:
        workflow = yaml.safe_load(f)
    return workflow

def get_all_workflows():
    """
    get_all_workflows Récupère tous les workflows disponibles
    :return: Liste de noms de workflows
    """
    workflows = {}
    for filename in os.listdir(WORKFLOWS_DIR):
        if filename.endswith('.yaml'):
            workflow_name = filename[:-5]  # Enlever l'extension .yaml
            workflow = load_workflow(workflow_name)
            workflows[workflow_name] = workflow
    return workflows

def resolve_workflow_order():
    workflows = get_all_workflows()
    visited = set()
    ordered_workflows = []
    rec_stack = set()

    # Séparez les workflows sans dépendances
    independent_workflows = [name for name, wf in workflows.items() if not wf.get('depends_on')]
    independent_workflows.sort()  # Tri par ordre alphabétique

    def visit(workflow_name):
        if workflow_name in rec_stack:
            # Dépendance circulaire détectée
            cycle = ' -> '.join(list(rec_stack) + [workflow_name])
            raise Exception(f"Dépendance circulaire détectée : {cycle}")
        if workflow_name in visited:
            return
        rec_stack.add(workflow_name)
        workflow = workflows[workflow_name]
        for dep in workflow.get('depends_on', []):
            visit(dep)
        rec_stack.remove(workflow_name)
        visited.add(workflow_name)
        ordered_workflows.append(workflow_name)

    # Visitez d'abord les workflows avec dépendances
    for workflow_name in workflows.keys():
        if workflows[workflow_name].get('depends_on'):
            visit(workflow_name)

    # Ajoutez ensuite les workflows indépendants triés
    ordered_workflows.extend(independent_workflows)

    return ordered_workflows