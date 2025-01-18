from base_module import BaseModule
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import re

class Module(BaseModule):
    def run(self, context):
        """
        Trouve et analyse les formulaires d'inscription sur le site
        """
        base_url = context.get('params', {}).get('url', context.get('target'))
        module_results = context.setdefault('module_results', [])
        
        if not base_url:
            module_results.append({
                'Password Form Analysis': {
                    'error': 'Aucune URL fournie'
                }
            })
            return context

        register_pages = self._find_register_pages(base_url)
        form_results = []

        for page in register_pages:
            result = self._analyze_page(page, context.get('params', {}))
            if result:
                form_results.append(result)

        module_results.append({
            'Password Form Analysis': {
                'base_url': base_url,
                'register_pages_found': len(register_pages),
                'forms_analyzed': len(form_results),
                'findings': form_results,
                'vulnerable': any(not r['secure'] for r in form_results if r),
                'recommendations': self._generate_recommendations(form_results)
            }
        })

        return context

    def _find_register_pages(self, base_url):
        """
        Recherche spécifiquement les pages d'inscription avec une approche complète
        """
        register_pages = set()
        common_paths = [
            '/signup.php', '/register.php', '/inscription.php',
            '/signup', '/register', '/inscription',
            '/signup.html', '/register.html', '/create-account',
            '/new-account', '/users/new', '/user/register',
            '/join', '/create', '/register/new'
        ]

        try:
            # 1. Vérifier les chemins communs
            for path in common_paths:
                test_url = urljoin(base_url, path)
                try:
                    response = requests.get(test_url, timeout=5)
                    if response.status_code == 200:
                        if self._is_register_page(response.text):
                            register_pages.add(test_url)
                except requests.RequestException:
                    continue

            # 2. Analyser la page principale
            response = requests.get(base_url)
            soup = BeautifulSoup(response.text, 'html.parser')

            # Patterns pour l'identification
            register_patterns = [
                r'register', r'signup', r'sign-up', r'inscription', 
                r'create[_-]account', r'nouveau[_-]compte', r'new[_-]user'
            ]

            # Recherche dans les liens
            for link in soup.find_all('a', href=True):
                href = link.get('href')
                text = link.get_text().lower()
                if self._matches_register_patterns(href, text, register_patterns):
                    full_url = urljoin(base_url, href)
                    register_pages.add(full_url)

            # Recherche dans les formulaires
            for form in soup.find_all('form'):
                action = form.get('action', '')
                if self._is_register_form(form):
                    full_url = urljoin(base_url, action)
                    register_pages.add(full_url)

        except requests.exceptions.RequestException as e:
            print(f"Erreur lors de la recherche des pages d'inscription : {e}")

        return list(register_pages)

    def _is_register_page(self, html_content):
        """
        Vérifie si une page est une page d'inscription
        """
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Vérifier le titre et les en-têtes
        title_text = ' '.join([
            t.get_text().lower() for t in soup.find_all(['title', 'h1', 'h2', 'h3'])
        ])
        
        register_keywords = [
            'sign up', 'signup', 'register', 'inscription', 
            'create account', 'new user', 'nouveau compte'
        ]

        if any(keyword in title_text for keyword in register_keywords):
            return True

        # Vérifier les champs de formulaire
        forms = soup.find_all('form')
        for form in forms:
            password_fields = form.find_all('input', type='password')
            email_field = form.find('input', type=['email', 'text'])
            
            if len(password_fields) >= 2 or (
                len(password_fields) >= 1 and
                email_field and
                any(keyword in form.get_text().lower() for keyword in register_keywords)
            ):
                return True

        return False

    def _analyze_page(self, url, params):
        """
        Analyse une page d'inscription
        """
        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            forms = soup.find_all('form')
            for form in forms:
                if self._is_register_form(form):
                    return self._analyze_form(form, url)
                    
        except requests.RequestException:
            return None

    def _is_register_form(self, form):
        """
        Vérifie si le formulaire est un formulaire d'inscription
        """
        # Vérifier les champs requis
        password_fields = form.find_all('input', type='password')
        has_password = len(password_fields) >= 1
        has_email = bool(form.find('input', type=['email', 'text']))
        
        # Vérifier le texte du formulaire
        form_text = form.get_text().lower()
        register_keywords = [
            'register', 'sign up', 'create account', 'inscription', 
            'nouveau compte', 'new user', 'signup'
        ]
        
        # Vérifier les noms des champs
        input_names = [i.get('name', '').lower() for i in form.find_all('input')]
        register_field_patterns = [
            'username', 'email', 'password', 'confirm', 'retype'
        ]

        return (
            has_password and 
            has_email and 
            (any(keyword in form_text for keyword in register_keywords) or
             any(pattern in ' '.join(input_names) for pattern in register_field_patterns))
        )

    def _analyze_form(self, form, url):
        """
        Analyse la sécurité d'un formulaire d'inscription
        """
        security_checks = {
            'has_password_field': False,
            'has_password_confirmation': False,
            'has_password_requirements': False,
            'has_minimum_length': False,
            'requires_special_chars': False,
            'requires_numbers': False,
            'requires_mixed_case': False
        }

        # Vérification des champs de mot de passe
        password_fields = form.find_all('input', type='password')
        security_checks['has_password_field'] = len(password_fields) > 0
        security_checks['has_password_confirmation'] = len(password_fields) > 1

        # Analyse du texte pour les exigences
        form_text = form.get_text().lower()
        
        # Recherche des exigences spécifiques
        security_checks['has_minimum_length'] = bool(
            re.search(r'\d+\s*(caractères|characters)', form_text)
        )
        security_checks['requires_special_chars'] = bool(
            re.search(r'(special|spécial|symbole)', form_text)
        )
        security_checks['requires_numbers'] = bool(
            re.search(r'(chiffre|number|digit)', form_text)
        )
        security_checks['requires_mixed_case'] = bool(
            re.search(r'(majuscule|uppercase|minuscule|lowercase)', form_text)
        )

        # Vérification globale des exigences
        security_checks['has_password_requirements'] = any([
            security_checks['has_minimum_length'],
            security_checks['requires_special_chars'],
            security_checks['requires_numbers'],
            security_checks['requires_mixed_case']
        ])

        return {
            'url': url,
            'secure': all([
                security_checks['has_password_field'],
                security_checks['has_password_confirmation'],
                security_checks['has_password_requirements']
            ]),
            'security_checks': security_checks
        }

    def _matches_register_patterns(self, href, text, patterns):
        """
        Vérifie si un lien correspond aux patterns d'inscription
        """
        text = text.lower()
        href = href.lower()
        
        return any(
            re.search(pattern, href) or re.search(pattern, text) 
            for pattern in patterns
        )

    def _generate_recommendations(self, results):
        """
        Génère des recommandations basées sur les résultats
        """
        recommendations = []
        for result in results:
            checks = result.get('security_checks', {})
            if not checks.get('has_password_confirmation'):
                recommendations.append("Ajouter un champ de confirmation de mot de passe")
            if not checks.get('has_minimum_length'):
                recommendations.append("Spécifier une longueur minimale pour le mot de passe")
            if not checks.get('requires_special_chars'):
                recommendations.append("Exiger des caractères spéciaux dans le mot de passe")
            if not checks.get('requires_numbers'):
                recommendations.append("Exiger des chiffres dans le mot de passe")
            if not checks.get('requires_mixed_case'):
                recommendations.append("Exiger des majuscules et minuscules dans le mot de passe")

        return list(set(recommendations))
