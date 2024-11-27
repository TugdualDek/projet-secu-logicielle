from base_module import BaseModule
import requests

def access_sensitive_resource(session, resource_url, expected_result):
  response = session.get(resource_url)
  if expected_result == "allowed":
    return response.status_code == 200
  elif expected_result == "denied":
    return response.status_code == 403
  else:
    return False
