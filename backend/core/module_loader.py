import importlib
import os
import sys

MODULES_DIR = "vulnerabilities/modules"

def load_modules():
    """
    load_modules Charge les modules disponibles
    :return: Dictionnaire de modules
    """
    modules = {}
    sys.path.insert(0, MODULES_DIR)
    for module_name in os.listdir(MODULES_DIR):
        if module_name.endswith('.py') and module_name != 'base_module.py':
            module_name = module_name[:-3]
            module = importlib.import_module(module_name)
            modules[module_name] = module.Module()
    sys.path.pop(0)
    return modules