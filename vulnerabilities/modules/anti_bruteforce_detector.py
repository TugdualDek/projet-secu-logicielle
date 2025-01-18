from vulnerabilities.modules.base_module import BaseModule
import re

class AntiBruteforceDetector:
    def detect(self, response):
        raise NotImplementedError("detect() must be implemented.")

    def adjust_strategy(self, protection_type):
        raise NotImplementedError("adjust_strategy() must be implemented.")

class DefaultAntiBruteforceDetector(AntiBruteforceDetector):
    def __init__(self):
        self.failure_patterns = {
            'captcha': r'captcha|recaptcha|verify you\'?re human',
            'rate_limit': r'too many attempts|rate limit|try again later|too many requests',
            'ip_block': r'ip.*blocked|access denied|forbidden'
        }
        self.protection_strategies = {
            'captcha': {'delay': 5, 'max_attempts': 3, 'action': 'abort'},
            'rate_limit': {'delay': 60, 'max_attempts': 5, 'action': 'wait'},
            'ip_block': {'delay': 600, 'max_attempts': 1, 'action': 'abort'}
        }

    def detect(self, response):
        if response.status_code in [403, 429]:
            return 'rate_limit'

        for protection_type, pattern in self.failure_patterns.items():
            if re.search(pattern, response.text, re.I):
                return protection_type
        return None

    def adjust_strategy(self, protection_type):
        return self.protection_strategies.get(
            protection_type,
            {'delay': 1, 'max_attempts': 20, 'action': 'continue'}
        )

class Module(BaseModule):
    def __init__(self):
        self.detector = DefaultAntiBruteforceDetector()

    def run(self, context):
        response = context.get('response')
        if not response:
            context.setdefault('errors', []).append("Aucune réponse à analyser")
            return context

        protection_type = self.detector.detect(response)
        if protection_type:
            strategy = self.detector.adjust_strategy(protection_type)
            context['anti_bruteforce'] = {
                'detected': True,
                'type': protection_type,
                'strategy': strategy
            }
        else:
            context['anti_bruteforce'] = {
                'detected': False
            }

        return context