from base_module import BaseModule
import requests

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
