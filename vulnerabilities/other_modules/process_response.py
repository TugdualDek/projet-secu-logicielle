from vulnerabilities.modules.base_module import BaseModule

class Module(BaseModule):
    def run(self, context):
        response = context.get('response')
        
        # Convertir expected_status en entier
        try:
            expected_status = int(context.get('expected_status'))
        except (TypeError, ValueError):
            raise ValueError("Le 'expected_status' doit être un entier.")

        if response.status_code == expected_status:
            context['status'] = 'success'
        else:
            context['status'] = 'failure'
        
        return context