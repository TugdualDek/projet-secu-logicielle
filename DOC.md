# Documentation du Scanner de Vulnérabilités Web
## Introduction
Bienvenue dans la documentation du scanner de vulnérabilités pour applications web. Ce scanner est conçu pour être hautement modulaire, permettant à quiconque d'ajouter facilement de nouveaux modules et workflows sans modifier le code de base. Le système est construit autour de deux concepts clés :

- **Modules** : Composants qui réalisent une action spécifique pour tester une vulnérabilité.
- **Workflows** : Séquences de modules orchestrés pour effectuer des tests de vulnérabilités complets.

Le scanner utilise un système de **contexte** pour partager des informations entre les modules au sein d'un workflow.
## Architecture Générale
### Le Système de Contexte
Le contexte est un dictionnaire Python qui persiste tout au long de l'exécution d'un workflow. Il permet :

- Le partage de données entre les modules.
- Le stockage des résultats des tests.
- La gestion des erreurs survenues lors de l'exécution.

Le contexte est initialisé en focntion de parmaetres insiqués dans les workflows ou données via l'api du scanner.

## Les Modules
### Structure d'un Module
Tous les modules doivent hériter de la classe abstraite BaseModule et implémenter la méthode run(context). 

**base_module.py** :
```python

from abc import ABC, abstractmethod

class BaseModule(ABC):
    @abstractmethod
    def run(self, context):
        """
        Méthode principale que chaque module doit implémenter.
        :param context: Dictionnaire contenant le contexte d'exécution.
        """
        pass
```

### Création d'un Module
Pour créer un nouveau module :

- Créer un fichier Python pour le module (par exemple, mon_module.py).
- Hériter de BaseModule.
- Implémenter la méthode run(context) pour réaliser l'action spécifique.
- Utiliser le contexte pour lire les entrées et stocker les sorties.

**Exemple minimal** :
```python

from base_module import BaseModule

class Module(BaseModule):
    def run(self, context):
        # Votre logique ici
        return context
```

### Gestion du Contexte

- Lire des données : ```url = context.get('url')```
- Stocker des résultats : ```context.setdefault('results', {})['nom_du_test'] = resultats```
- Enregistrer des erreurs : ```context.setdefault('errors', []).append("Message d'erreur")```
- Partager des données : ```context['clé'] = valeur```

### Exemples de Modules
**http_request.py**

Ce module effectue une requête HTTP vers une URL cible et stocke la réponse dans le contexte.

```python
from base_module import BaseModule
import requests

class Module(BaseModule):
    def run(self, context):
        url = context.get('url')
        timeout = context.get('timeout', 5)
        try:
            response = requests.get(url, timeout=timeout)
            context['response_headers'] = dict(response.headers)
            context['response_cookies'] = response.cookies
        except requests.RequestException as e:
            context.setdefault('errors', []).append(f"Échec de la requête HTTP : {e}")
        return context
```

**analyze_headers.py**

Ce module analyse les en-têtes de sécurité dans la réponse HTTP.
```python

from base_module import BaseModule

class Module(BaseModule):
    def run(self, context):
        headers = context.get('response_headers')
        if not headers:
            context.setdefault('errors', []).append("Aucune en-tête trouvée pour l'analyse.")
            return context

        security_headers = [
            'Strict-Transport-Security',
            'Content-Security-Policy',
            'X-Content-Type-Options',
            'X-Frame-Options',
            'X-XSS-Protection',
            'Referrer-Policy',
            'Permissions-Policy'
        ]

        results = {}
        for header in security_headers:
            value = headers.get(header)
            results[header] = {
                'present': value is not None,
                'value': value
            }

        context.setdefault('results', {})['security_headers_analysis'] = results
        return context
```

**analyze_cookies.py**

Ce module analyse les attributs de sécurité des cookies reçus dans la réponse.
```python
from http.cookies import SimpleCookie
from base_module import BaseModule

class Module(BaseModule):
    def run(self, context):
        cookies = context.get('response_cookies')
        if not cookies:
            context.setdefault('results', {})['cookies_analysis'] = "Aucun cookie trouvé."
            return context

        cookie_parser = SimpleCookie()
        cookie_parser.load(cookies)

        results = {}
        for morsel in cookie_parser.values():
            cookie_name = morsel.key
            attributes = {
                'Secure': 'secure' in morsel['secure'].lower(),
                'HttpOnly': 'httponly' in morsel['httponly'].lower(),
                'SameSite': morsel.get('samesite', 'None')
            }
            results[cookie_name] = attributes

        context.setdefault('results', {})['cookies_analysis'] = results
        return context
```

**cors_tester.py**

Ce module teste la configuration CORS du site en envoyant des requêtes avec différents domaines d'origine.
```python

from base_module import BaseModule
import requests

class Module(BaseModule):
    def run(self, context):
        url = context.get('url')
        test_origins = context.get('test_origins', ['http://evil.com', 'null'])
        results = []

        for origin in test_origins:
            headers = {'Origin': origin}
            try:
                response = requests.get(url, headers=headers)
                acao = response.headers.get('Access-Control-Allow-Origin')
                misconfig = acao == '*' or acao == origin
                results.append({
                    'origin': origin,
                    'misconfiguration': misconfig,
                    'acao': acao
                })
            except requests.RequestException as e:
                results.append({
                    'origin': origin,
                    'error': str(e)
                })

        context.setdefault('results', {})['cors_analysis'] = results
        return context
```

### Bonnes Pratiques

- Retourner le contexte : Assurez-vous que votre module retourne le contexte modifié.
- Gérer les exceptions : Utilisez des blocs try-except pour capturer les erreurs.
- Utiliser le contexte : Évitez d'utiliser des variables globales ou de stocker des états en dehors du contexte.

## Les Workflows
### Structure d'un Workflow
Un workflow est défini dans un fichier YAML et décrit une séquence d'étapes à exécuter. Exemple de test_workflow.yaml :
```yaml

name: security_headers_cookies_cors_workflow
description: Vérification des en-têtes de sécurité, des cookies et de la configuration CORS
steps:
  - module: http_request
    params:
      url: "{{ target }}"
      timeout: 10
  - module: analyze_headers
  - module: analyze_cookies
  - module: cors_tester
    params:
      test_origins:
        - "{{ target }}"
        - "http://evil.com"
        - "null"
```

### Éléments du Workflow

- name : Nom unique du workflow.
- description : Description du but du workflow.
- steps : Liste ordonnée des modules à exécuter.

### Utilisation des Paramètres

- Paramètres statiques : Valeurs définies directement dans le workflow.
- Paramètres dynamiques : Utilisation de variables avec la syntaxe {{ variable }} qui seront remplacées à l'exécution.

### Création d'un Workflow
Pour créer un nouveau workflow :

1. Créer un fichier YAML nommé de manière appropriée (par exemple, mon_workflow.yaml).
2. Définir le nom et la description du workflow.
3. Listez les étapes en spécifiant le module et les paramètres pour chaque étape.

Exemple :
```yaml

name: test_mon_module
description: Workflow pour tester mon nouveau module
steps:
  - module: http_request
    params:
      url: "{{ target }}"
  - module: mon_module
    params:
      param1: "valeur1"
      param2: "{{ variable_dynamique }}"
```

### Exécution du Workflow
Lors de l'exécution :

- Initialisation du contexte avec les variables globales et les paramètres fournis.
- Exécution séquentielle des modules selon l'ordre défini dans le workflow.
- Mise à jour du contexte après chaque module.
- Collecte des résultats et erreurs pour le rapport final.

## Décomposition des Tests en Modules
Lors de la création de tests pour des vulnérabilités complexes, il est préférable de les décomposer en **plusieurs modules**. Cela permet :

- La réutilisation des modules pour différents workflows.
- Une meilleure maintenance en isolant les fonctionnalités.
- Une flexibilité accrue pour combiner différentes actions.

Exemple :

- Module 1 : Envoyer une requête avec un payload spécifique.
- Module 2 : Analyser la réponse pour détecter des signes de vulnérabilité.
- Module 3 : Enregistrer les résultats dans le contexte.

## Exemple Complet
**Nouveau Module : xss_tester.py**
```python

from base_module import BaseModule
import requests

class Module(BaseModule):
    def run(self, context):
        url = context.get('url')
        payloads = context.get('payloads', ['<script>alert(1)</script>', '" onmouseover="alert(1)"'])
        results = []

        for payload in payloads:
            params = {'input': payload}
            try:
                response = requests.get(url, params=params)
                if payload in response.text:
                    results.append({
                        'payload': payload,
                        'vulnerable': True
                    })
                else:
                    results.append({
                        'payload': payload,
                        'vulnerable': False
                    })
            except requests.RequestException as e:
                context.setdefault('errors', []).append(f"Erreur lors du test XSS avec payload {payload}: {e}")

        context.setdefault('results', {})['xss_test'] = results
        return context
```

**Nouveau Workflow : xss_workflow.yaml**
```yaml

name: xss_test_workflow
description: Workflow pour tester les failles XSS
steps:
  - module: xss_tester
    params:
      url: "{{ target }}"
      payloads:
        - "<script>alert(1)</script>"
        - "'\"><img src=x onerror=alert(1)>"
```

## Conclusion
Cette documentation vous guide dans la création de modules et de workflows pour enrichir votre scanner de vulnérabilités web. En tirant parti de la modularité du système, vous pouvez adapter et étendre les tests pour couvrir un large éventail de vulnérabilités.

**Points Essentiels** :

- Modularité : Les modules exécutent des actions unitaires spécifiques.
- Flexibilité : Les workflows orchestrent les modules pour réaliser des tests complexes.
- Extensibilité : Ajoutez facilement de nouveaux tests sans modifier le code de base.

**Bonnes Pratiques** :

- Clarté du Code : Commentez et structurez bien votre code pour faciliter la compréhension.
- Réutilisation : Concevez les modules pour qu'ils puissent être réutilisés dans différents workflows.
- Gestion des Erreurs : Capturez et enregistrez les erreurs pour faciliter le débogage.

## Exemple de Contexte Après Exécution
```python

{
    'url': 'http://exemple.com',
    'results': {
        'security_headers_analysis': {
            'Strict-Transport-Security': {'present': True, 'value': 'max-age=63072000; includeSubDomains'},
            # Autres en-têtes...
        },
        'cookies_analysis': {
            'sessionid': {
                'Secure': True,
                'HttpOnly': True,
                'SameSite': 'Lax'
            }
            # Autres cookies...
        },
        'cors_analysis': [
            {
                'origin': 'http://evil.com',
                'misconfiguration': False,
                'acao': 'null'
            }
            # Autres résultats...
        ]
    },
    'errors': []
}
```

N'hésitez pas à contribuer en ajoutant vos propres modules et workflows pour améliorer continuellement le scanner.