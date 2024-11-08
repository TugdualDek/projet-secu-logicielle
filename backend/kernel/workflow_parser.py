import yaml
import os

WORKFLOWS_DIR = os.path.join(os.path.dirname(__file__), 'workflows')

def load_workflow(workflow_name):
    workflow_file = os.path.join(WORKFLOWS_DIR, f"{workflow_name}.yaml")
    with open(workflow_file, 'r') as f:
        workflow = yaml.safe_load(f)
    return workflow