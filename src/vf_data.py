import datetime
import json
from operator import itemgetter

import requests
import hashlib
import logging
import getConfig
import dbdata


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

def get_starts_by_date_and_name(date, vname, nname):
    """
        This function is used to get the starts of a user by their first and last name and a date.
        IMPORTANT: THIS FUNCTION REQUIRES THE RIGHT "Mitgliederdaten bearbeiten"/"Edit member data"

        Parameters:
        vname (str): The first name of the user.
        nname (str): The last name of the user.
        date (str): The date in the format "dd.mm.yyyy".

        Returns:
        List[str]: The starts of the user if found, otherwise an empty list.
        """
    logging.info('getting starts for ' + vname + ' ' + nname + '...')
    try:
        accesstoken = login()
        url = _api_url + "interface/rest/flight/list/date"
        payload = {
            'accesstoken': accesstoken,
            "dateparam": date,
        }
        response = requests.post(url, data=json.dumps(payload))
        response_code = response.status_code
        response_data =response.json()
        if response_code != 200:
            raise ConnectionError("Server returned " + str(response.status_code))
        startcounter = 0
        for flight in response_data.values():
            try:
                if flight.get('starttype') == '5' and flight.get('pilotname') == nname + ", " + vname:
                    startcounter += 1
            except AttributeError:
                logging.debug("reached end of list")
        return startcounter
    except ConnectionError:
        logging.error("Error while getting starts returning empty list")
        return 0


def get_starts_by_date_and_id(date, uid):
    """
            This function is used to get the starts of a user by their first and last name and a date.
            IMPORTANT: THIS FUNCTION REQUIRES THE RIGHT "Mitgliederdaten bearbeiten"/"Edit member data"

            Parameters:
            uid (int): The member ID of the user.
            date (str): The date in the format "dd.mm.yyyy".

            Returns:
            List[str]: The starts of the user if found, otherwise an empty list.
            """
    vname = dbdata.get_vname_by_id(uid)
    nname = dbdata.get_nname_by_id(uid)
    logging.info('getting starts for ' + vname + ' ' + nname + '...')
    try:
        accesstoken = login()
        url = _api_url + "interface/rest/flight/list/date"
        payload = {
            'accesstoken': accesstoken,
            "dateparam": date,
        }
        response = requests.post(url, data=json.dumps(payload))
        response_code = response.status_code
        response_data = response.json()
        if response_code != 200:
            raise ConnectionError("Server returned " + str(response.status_code))
        startcounter = 0
        for flight in response_data.values():
            try:
                if flight.get('starttype') == '5' and flight.get('pilotname') == nname + ", " + vname:
                    startcounter += 1
            except AttributeError:
                logging.debug("reached end of list")
        return startcounter
    except ConnectionError:
        logging.error("Error while getting starts returning empty list")
        return 0

def get_starts_by_multiple_dates_and_id(startdate, enddate, uid):
        """
                This function is used to get the starts of a user by their first and last name and a date.
                IMPORTANT: THIS FUNCTION REQUIRES THE RIGHT "Mitgliederdaten bearbeiten"/"Edit member data"

                Parameters:
                uid (int): The member ID of the user.
                date (str): The date in the format "dd.mm.yyyy".

                Returns:
                List[str]: The starts of the user if found, otherwise an empty list.
                """
        print(enddate)
        print(startdate)
        startdate_obj = datetime.datetime.strptime(startdate, "%d.%m.%Y")
        startdate_year = startdate_obj.year
        startdate_month = startdate_obj.month
        startdate_day = startdate_obj.day
        startdate_final = datetime.date(startdate_year, startdate_month, startdate_day)
        enddate_obj = datetime.datetime.strptime(enddate, "%d.%m.%Y")
        enddate_year = enddate_obj.year
        enddate_month = enddate_obj.month
        enddate_day = enddate_obj.day
        enddate_final = datetime.date(enddate_year, enddate_month, enddate_day)
        delta = datetime.timedelta(days=1)
        vname = dbdata.get_vname_by_id(uid)
        nname = dbdata.get_nname_by_id(uid)
        logging.info('getting starts for ' + vname + ' ' + nname + '...')
        accesstoken = login()
        url = _api_url + "interface/rest/flight/list/date"
        startcounter_array= {}
        while startdate_final <= enddate_final:
            try:
                payload = {
                    'accesstoken': accesstoken,
                    "dateparam": str(startdate_final),
                }
                response = requests.post(url, data=json.dumps(payload))
                response_code = response.status_code
                response_data = response.json()
                if response_code != 200:
                    raise ConnectionError("Server returned " + str(response.status_code))
                startcounter_winch = 0
                startcounter_landing = 0
                for flight in response_data.values():
                    try:
                        if flight.get('starttype') == '5' and flight.get('pilotname') == nname + ", " + vname:
                            startcounter_winch += 1
                        if flight.get('starttype') == '1' and flight.get('pilotname') == nname + ", " + vname:
                            landing_sum = flight.get('landingcount')
                            startcounter_landing += int(landing_sum)
                    except AttributeError:
                        logging.debug("reached end of list")
                if startcounter_winch > 0:
                    startdate_final_str = startdate_final.strftime("%d.%m.%Y")
                    startcounter_array[startdate_final_str]= str(startcounter_winch) + " Winde"
                if startcounter_landing > 0:
                    startdate_final_str = startdate_final.strftime("%d.%m.%Y")
                    startcounter_array[startdate_final_str]= str(startcounter_landing) + " Eigen"
            except ConnectionError:
                logging.error("Error while getting starts returning empty list")
            finally:
                startdate_final += delta

        print(startcounter_array)
        return startcounter_array