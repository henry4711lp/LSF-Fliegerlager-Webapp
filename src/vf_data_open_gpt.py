import logging

import requests
import hashlib
import getConfig

_api_token = getConfig.get_config("api_token")
_api_username = getConfig.get_config("api_username")
_api_password = getConfig.get_config("api_password")
_api_url = getConfig.get_config("api_url")


def get_access_token():
    url = _api_url + "interface/rest/auth/accesstoken"
    response = requests.get(url)
    logging.debug(f"Got accesstoken: {response.json()['accesstoken']}")
    return response.json()["accesstoken"]


def sign_in(username, password):
    url = _api_url + "interface/rest/auth/signin"
    password = hashlib.md5(password.encode('utf-8')).hexdigest()
    auth_secret = input('Enter auth_secret:')
    data = {
        "accesstoken": access_token,
        "username": username,
        "password": password,
        "appkey": _api_token,
        "auth_secret": auth_secret
    }
    response = requests.post(url, data=data)
    logging.debug(f"Sign in got response: {response.json()}")


def find_member_number(firstname, lastname):
    url = _api_url + "interface/rest/auth/getuser"
    data = {
        "accesstoken": access_token
    }
    response = requests.post(url, data=data)
    if response.status_code == 200:
        user_data = response.json()
        return user_data
    else:
        return None


def sign_out():
    url = _api_url + "interface/rest/auth/signout"
    data = {
        "accesstoken": access_token
    }
    response = requests.delete(url, data=data)
    logging.debug(f"Sign out got response: {response}")


access_token = get_access_token()
print(access_token)
sign_in(_api_username, _api_password)
member_number = find_member_number("John", "Doe")
print(member_number)
sign_out()
