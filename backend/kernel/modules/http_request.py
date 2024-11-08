
from base_module import BaseModule
import requests

class Module(BaseModule):
    def run(self, context):
        url = context.get('url')
        response = requests.get(url)
        context['response'] = response
        return context