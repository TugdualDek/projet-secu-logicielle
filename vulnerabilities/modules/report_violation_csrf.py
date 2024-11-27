from base_module import BaseModule

def report_violation(violation_type, vulnerable_url, details=""):
  print(f"Vulnérabilité CSRF détectée !")
  print(f"  URL vulnérable: {vulnerable_url}")
  if details:
    print(f"  Détails: {details}")
