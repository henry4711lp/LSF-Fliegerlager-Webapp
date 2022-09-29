import json
import requests
import hashlib
from src import getConfig


# Get the data from the API
def get_access_token(x):
    url = _api_url + "interface/rest/auth/accesstoken"
    response = requests.get(url)
    data = response.json()
    return data.get(x)


_api_token = getConfig.getConfig("api_token")
_api_username = getConfig.getConfig("api_username")
_api_password = getConfig.getConfig("api_password")
_api_url = getConfig.getConfig("api_url")


def test():
    print(_api_token)


def login():
    print('logging user ' + _api_username + ' in...')
    # post to api with username and password and api_token
    url = _api_url + "interface/rest/auth/login"
    auth_secret = input('Enter auth_secret: ')
    payload = {
        'accesstoken': get_access_token("accesstoken"),
        "username": _api_username,
        "password": hashlib.md5(_api_password.encode()).hexdigest(),
        "appkey": _api_token,
        "auth_secret": auth_secret
    }
    print(json.dumps(payload, indent=4))
    response = requests.post(url, data=json.dumps(payload))
    data = response.json()
    return data
