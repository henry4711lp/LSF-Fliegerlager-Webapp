import requests
import hashlib
import configparser

config = configparser.ConfigParser()
config.read("config.ini")

API_URL = config.get("api", "url")
API_KEY = config.get("api", "key")
USERNAME = config.get("user", "username")
PASSWORD = config.get("user", "password")

def get_access_token():
  url = API_URL + "/auth/accesstoken"
  response = requests.get(url)
  return response.json()["accesstoken"]

def sign_in(username, password):
  url = API_URL + "/auth/signin"
  password = hashlib.md5(password.encode('utf-8')).hexdigest()
  data = {
    "accesstoken": access_token,
    "username": username,
    "password": password,
    "appkey": API_KEY
  }
  response = requests.post(url, data=data)

def find_member_number(firstname, lastname):
  url = API_URL + "/auth/getuser"
  data = {
    "accesstoken": access_token
  }
  response = requests.post(url, data=data)
  if response.status_code == 200:
    user_data = response.json()
    return user_data["memberid"]
  else:
    return None

def sign_out():
  url = API_URL + "/auth/signout"
  data = {
    "accesstoken": access_token
  }
  response = requests.delete(url, data=data)

access_token = get_access_token()
sign_in(USERNAME, PASSWORD)
member_number = find_member_number("John", "Doe")
print(member_number)
sign_out()
