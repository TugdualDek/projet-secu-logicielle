from base_module import BaseModule

def report_violation(violation_type, username, resource_url):
  print(f"Violation du principe du moindre privilège détectée !")
  print(f"  Type de violation: {violation_type}")
  print(f"  Utilisateur: {username}")
  print(f"  Ressource: {resource_url}")
