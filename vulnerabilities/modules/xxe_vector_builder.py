from vulnerabilities.modules.base_module import BaseModule

class Module(BaseModule):
    def run(self, context):
        endpoints = context.get('discovered_endpoints', [])
        module_results = context.setdefault('module_results', [])

        xxe_candidates = []

        # Par exemple, on choisit des endpoints POST et on suppose qu'ils peuvent traiter du XML
        # Tu peux ajouter des critères plus complexes :
        # - Filtrer par URL (ex: qui contiennent "xml" dans l'URL)
        # - Vérifier le Content-Type attendu (si tu as cette info quelque part)

        for ep in endpoints:
            url = ep.get('url')
            method = ep.get('method', 'get').lower()

            # On suppose que seuls les endpoints POST sont intéressants pour du XML
            # et que l'URL contient "xml"
            if method == 'post' and 'xml' in url.lower():
                xxe_candidates.append({'url': url})

        if xxe_candidates:
            module_results.append({'XXE Vector Builder': 'Endpoints XML testables trouvés.'})
        else:
            module_results.append({'XXE Vector Builder': 'Aucun endpoint XML trouvé.'})

        # On stocke les vecteurs dans le contexte
        context['xxe_vectors'] = xxe_candidates

        return context
