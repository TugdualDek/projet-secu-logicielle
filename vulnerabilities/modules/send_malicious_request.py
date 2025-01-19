from base_module import BaseModule
import requests

class Module(BaseModule):
<<<<<<< HEAD
  def send_malicious_request(session, vulnerable_url, attack_parameter, attack_value):
    try:
      if session:
        response = session.post(vulnerable_url, data={attack_parameter: attack_value})
      else:
        response = requests.post(vulnerable_url, data={attack_parameter: attack_value})
      return True
    except requests.exceptions.RequestException as e:
      print(f"Error while sending request : {e}")
      return False
=======
  def run(self, context):
    try:
        vulnerable_url = context.get('target')
        if not vulnerable_url:
            raise ValueError("URL manquante dans le contexte pour envoyer la requête malveillante.")
        session = context.get('session')
        attack_parameter = context.get('attack_parameter')
        attack_value = context.get('attack_value')
        poc_html = context.get('poc_html')

        if not all([vulnerable_url, attack_parameter, attack_value, poc_html]):
            raise ValueError("Informations manquantes dans le contexte pour envoyer la requête malveillante.")

        if session:
            response = session.post(vulnerable_url, data={attack_parameter: attack_value}, files={'poc': poc_html})
        else:
            response = requests.post(vulnerable_url, data={attack_parameter: attack_value}, files={'poc': poc_html})

        context['request_status'] = response.status_code
        context['response_content'] = response.text
        return context

    except requests.exceptions.RequestException as e:
        context.setdefault('errors', []).append(f"Erreur lors de l'envoi de la requête : {e}")
        return context
    except Exception as e:
        context.setdefault('errors', []).append(f"Erreur dans send_malicious_request : {e}")
        return context
>>>>>>> refs/remotes/origin/bruce
