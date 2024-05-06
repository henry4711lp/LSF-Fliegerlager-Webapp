import json
import requests
import hashlib
import logging
import getConfig


# Get the data from the API
def get_access_token():
    """
        This function is used to get the access token from the API.

        It sends a GET request to the API endpoint for access tokens.
        The function returns the access token if the request is successful.

        Raises:
        ConnectionRefusedError: If the server returns a 401 status code, indicating unauthorized access.
        ConnectionError: If the server returns a 500 or greater status code, indicating an internal server error.
        ConnectionError: If the server returns any other status code.

        Returns:
        str: The access token if the request is successful.
        """
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


def login():
    """
        This function is used to log in a user using the API.
        WARNING: The password is hashed using MD5 before being sent.
        WARNING: The password is stored in plain text in the config file.
        WARNING: 2FA is implemented but not working with a functional user.

        It sends a POST request to the API with the username, password, and API token.
        The password is hashed using MD5 before being sent.
        The function returns the access token if the login is successful.

        Raises:
        ConnectionRefusedError: If the server returns a 401 status code, indicating unauthorized access.
        ConnectionError: If the server returns a 500 or greater status code, indicating an internal server error.
        ConnectionError: If the server returns any other status code.

        Returns:
        str: The access token if the login is successful.
        """
    logging.info('logging user ' + _api_username + ' in...')
    # post to api with username and password and api_token
    url = _api_url + "interface/rest/auth/signin"
    #auth_secret = input('Enter auth_secret: ')
    accesstoken = get_access_token()
    password = hashlib.md5(_api_password.encode()).hexdigest()
    payload = {
        'accesstoken': accesstoken,
        "username": _api_username,
        "password": password,
        "appkey": _api_token,
        "cid":  _api_cid,
        #"auth_secret": auth_secret
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


def get_vfid(vname, nname):
    """
        This function is used to get the member ID of a user by their first and last name.
        IMPORTANT: THIS FUNCTION REQUIRES THE RIGHT "Mitgliederdaten bearbeiten"/"Edit member data"

        Parameters:
        vname (str): The first name of the user.
        nname (str): The last name of the user.

        Returns:
        int: The member ID of the user if found, otherwise 1.
        """
    logging.info('getting vfid for ' + vname + ' ' + nname + '...')
    try:
        accesstoken = login()
        url = _api_url + "interface/rest/user/list"
        payload = {
            'accesstoken': accesstoken,
        }
        response = requests.post(url, data=json.dumps(payload))
        if response.status_code != 200:
            raise ConnectionError("Server returned " + str(response.status_code))
        for user in response.json().get("users"):
            if user.get("firstname") == vname and user.get("lastname") == nname:
                return user.get("memberid")
    except ConnectionError:
        logging.error("Error while getting vfid returning internal ID")
        return 1
