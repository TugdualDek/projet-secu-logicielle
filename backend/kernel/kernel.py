from backend.kernel.modules import load_modules

class Kernel:
    def __init__(self):
        self.modules = load_modules()

    def execute_workflow(self, workflow, context):
        for step in workflow:
            module_name = step['module']
            params = step.get('params', {})
            context.update(params)
            module = self.modules.get(module_name)
            if module:
                context = module.run(context)
            else:
                raise Exception(f"Module {module_name} not found")
        return context