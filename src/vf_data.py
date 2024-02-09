import json
import requests
import hashlib
import logging
import getConfig


# Get the data from the API
def get_access_token():
    url = _api_url + "interface/rest/auth/accesstoken"
    response = requests.get(url)
    data = response.json()
    return data.get("accesstoken")


_api_token = getConfig.get_config("api_token")
_api_username = getConfig.get_config("api_username")
_api_password = getConfig.get_config("api_password")
_api_url = getConfig.get_config("api_url")
_api_cid = getConfig.get_config("api_cid")


def test():
    print(_api_token)


def login(uname, pword, twofa):
    logging.info('logging user ' + _api_username + ' in...')
    # post to api with username and password and api_token
    url = _api_url + "interface/rest/auth/signin"
    auth_secret = twofa
    accesstoken = get_access_token()
    password = hashlib.md5(_api_password.encode()).hexdigest()
    payload = {
        'accesstoken': accesstoken,
        "username": uname,
        "password": pword,
        "appkey": _api_token,
        "cid":  _api_cid,
        "auth_secret": auth_secret
    }
    logging.debug('Password: ')
    logging.debug(password)
    logging.debug('Accesstoken' + str(accesstoken))
    logging.debug(json.dumps(payload, indent=4))
    response = requests.post(url, data=json.dumps(payload))
    if response.status_code == 200:
        return accesstoken
    elif response.status_code == 401:
        raise ConnectionRefusedError("Server returned 401, UNAUTHORIZED")
    elif response.status_code >= 500:
        raise ConnectionError("Server returned 500 or greater, INTERNAL SERVER ERROR: " + str(response.status_code))
    else:
        raise ConnectionError("Server returned " + str(response.status_code))


def get_vfid(vname, nname, twofa):
    logging.info('getting vfid for ' + vname + ' ' + nname + '...')
    try:
        accesstoken = login(vname, nname, twofa)
        url = _api_url + "interface/rest/auth/getuser"
        payload = {
            'accesstoken': accesstoken,
        }
        response = requests.post(url, data=json.dumps(payload))
        return response.json()
    except ConnectionError:
        logging.error("Error while getting vfid")
        return 1
