import yaml
import os

WORKFLOWS_DIR = "backend/scanner/workflows"

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
    workflows = []
    for filename in os.listdir(WORKFLOWS_DIR):
        if filename.endswith('.yaml'):
            workflow_name = filename[:-5]  # Enlever l'extension .yaml
            workflows.append(workflow_name)
    return workflows