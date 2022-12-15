import json
import requests
import hashlib
import logging
import getConfig


# Get the data from the API
def get_access_token(x):
    url = _api_url + "interface/rest/auth/accesstoken"
    response = requests.get(url)
    data = response.json()
    return data.get(x)


_api_token = getConfig.get_config("api_token")
_api_username = getConfig.get_config("api_username")
_api_password = getConfig.get_config("api_password")
_api_url = getConfig.get_config("api_url")


def test():
    print(_api_token)


def login():
    logging.info('logging user ' + _api_username + ' in...')
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
    logging.debug(json.dumps(payload, indent=4))
    response = requests.post(url, data=json.dumps(payload))
    data = response.json()
    return data


def get_vfid(vname, nname):
    logging.info('getting vfid for ' + vname + ' ' + nname + '...')
    return 0
