import datetime
import json
import logging

import mysql
from flask import redirect, url_for
from mysqlx.helpers import escape

import dbconnector
import formatprices
import getConfig
import vf_data


def get_all_data_of_uid():
    return dbconnector.sql("SELECT * FROM ID;")


def get_all_data_of_name():
    return dbconnector.sql("SELECT * FROM NAME;")


def get_all_data_of_ess():
    return dbconnector.sql("SELECT * FROM ESS;")


def get_all_data_of_getr():
    return dbconnector.sql("SELECT * FROM GETR;")


def get_all_data_of_persget():
    return dbconnector.sql("SELECT * FROM PERSGET;")


def get_all_data_of_persess():
    return dbconnector.sql("SELECT * FROM PERSESS;")


def get_all_data_of_stay():
    return dbconnector.sql("SELECT * FROM STAY;")


def get_id_by_name(vname, nname):
    """
This function takes a first and last name as inputs and returns the ID associated with that name in the NAME table of
the database.

Args:
    vname (str): The first name of the individual.
    nname (str): The last name of the individual.
    
Returns:
    The ID associated with the input name in the NAME table of the database.
"""
    sql_statement = "SELECT ID FROM NAME WHERE VNAME = '" + escape(vname) + "' AND NNAME = '" + escape(nname) + "'"
    return dbconnector.sql(sql_statement)


def get_vfid_by_name_from_vf(vname, nname):
    """
This function takes a first and last name as inputs and returns the VFID associated with that name in the VF table of the database.

Args:
    vname (str): The first name of the individual.
    nname (str): The last name of the individual.
    
Returns:
    The VFID associated with the input name in the VF table of the database.
"""
    return vf_data.get_vfid(vname, nname)


def get_eid_by_date(date):
    """
This function takes a date as input and returns the EID associated with that date in the ESS table of the database.

Args:
    date (str): The date to search for in the database.
    
Returns:
    The EID associated with the input date in the ESS table of the database.
"""
    sql_statement = "SELECT EID FROM ESS WHERE EDAT = '" + date + "'"
    eid = dbconnector.sql(sql_statement)
    if not eid:
        set_eid_with_date()
        sql_statement = "SELECT EID FROM ESS WHERE EDAT = '" + date + "'"
        eid = dbconnector.sql(sql_statement)
    return eid


def get_gpreis_by_gid(gid):
    """
This function takes a GID as input and returns the GPREIS associated with that GID in the GETR table of the database.

Args:
    gid (str): The GID to search for in the database.
    
Returns:
    The GPREIS associated with the input GID in the GETR table of the database.
"""
    sql_statement = "SELECT GPREIS FROM GETR WHERE GID = '" + escape(gid) + "'"
    return dbconnector.sql(sql_statement)


def get_all_gpreis():
    """
This function retrieves all GPREIS values from the GETR table in the database.

Returns:
    All GPREIS values from the GETR table in the database.
"""
    sql_statement = "SELECT GPREIS FROM GETR;"
    return dbconnector.sql(sql_statement)


def get_persess_by_id_and_eid(pid, eid):
    """
    This function retrieves data from the 'PERSESS' table in the database for a specific user ID and event ID.

    Args:
        pid (int): The user ID to search for in the database.
        eid (int): The event ID to search for in the database.

    Returns:
        list: A list containing the result of the SQL query. If the query is successful, the list will contain the data
        associated with the given user ID and event ID from the 'PERSESS' table. If the query fails, the list will be empty.

    Raises:
        RedirectException: If the provided user ID is None or not an integer, the function will redirect to the 'register' page.
    """
    if not eid or not isinstance(eid, int):
        set_eid_with_date()
    sql_statement = "SELECT * FROM PERSESS WHERE ID = '" + escape(pid) + "' AND EID = '" + str(eid) + "'"
    sql_result = dbconnector.sql(sql_statement)
    if not sql_result:
        sql_statement = "INSERT INTO PERSESS VALUES ('" + escape(pid) + "', '" + str(eid) + "', 0, 0, 0, 0)"
        dbconnector.sql(sql_statement)
        sql_statement = "SELECT * FROM PERSESS WHERE ID = '" + escape(pid) + "' AND EID = '" + str(eid) + "'"
        sql_result = dbconnector.sql(sql_statement)
    return sql_result


def get_persget_by_id_and_gid(pid, gid):
    """
This function takes a PID and GID as inputs and returns the corresponding entry in the PERSGET table of the database.

Args:
    pid (str): The PID to search for in the database.
    gid (str): The GID to search for in the database.
    
Returns:
    The entry in the PERSGET table of the database associated with the input PID and GID.
"""
    try:
        sql_statement = "SELECT CT FROM PERSGET WHERE ID = '" + str(pid) + "' AND GID = '" + str(gid) + "'"
        sql_result = dbconnector.sql(sql_statement)[0][0]
    except IndexError:
        sql_statement = "INSERT INTO PERSGET VALUES ('" + str(pid) + "', '" + str(gid) + "', 0)"
        dbconnector.sql(sql_statement)
        sql_result = 0
    return sql_result


def get_gprice_by_id(gid):
    """
This function takes a GID as input and returns the GPREIS associated with that GID in the GETR table of the database, formatted as a price.

Args:
    gid (str): The GID to search for in the database.
    
Returns:
    The GPREIS associated with the input GID in the GETR table of the database, formatted as a price.
"""
    sql_statement = "SELECT GPREIS FROM GETR WHERE GID = " + gid
    value = dbconnector.sql(sql_statement)
    value = json.loads(json.dumps(value))
    try:
        value = value[0][0]
    except IndexError:
        logging.error("Table is empty")
        value = 0
    return formatprices.format_prices(float(value))


def get_sum_of_drink_by_id_and_gid(uid, gid):
    """
This function takes a UID and GID as inputs and returns the total cost of all instances of the specified drink consumed by the specified user.

Args:
    uid (str): The UID to search for in the database.
    gid (str): The GID to search for in the database.
    
Returns:
    The total cost of all instances of the specified drink consumed by the specified user, formatted as a price.
"""
    sql_statement = f"SELECT GPREIS*CT FROM PERSGET NATURAL JOIN GETR WHERE ID = {uid} AND GID = {gid}"
    value = dbconnector.sql(sql_statement)
    value = json.loads(json.dumps(value))
    try:
        value = value[0][0]
    except IndexError:
        logging.error("Table is empty")
        value = 0
    return formatprices.format_prices(value)


# print the sum of all prices of all drinks of a user
def get_sum_of_drinks_by_id(uid):
    """
This function takes a UID as input and returns the total cost of all drinks consumed by the specified user.

Args:
    uid (str): The UID to search for in the database.
    
Returns:
    The total cost of all drinks consumed by the specified user.
"""
    sql_statement = f"SELECT GID,CT FROM PERSGET NATURAL JOIN GETR WHERE ID = {uid}"
    count = json.loads(json.dumps(dbconnector.sql(sql_statement)))
    full_price = 0
    price = json.loads(json.dumps(get_all_gpreis()))
    logging.debug(f"price: {price}")
    logging.debug(f"count: {count}")
    for i in range(0, len(count)):
        gid = count[i][0]
        counter = count[i][1]
        thisprice = price[i][0]
        logging.debug(f"Price of {gid} is {thisprice} and count is {counter}")
        cost_of_drink = thisprice * counter
        logging.debug(f" cost of drink  {cost_of_drink}")
        full_price += cost_of_drink
        logging.debug(f"Momentary full price  {full_price}")
    logging.debug(full_price)
    return full_price


# print the sum of all prices of all meals of a user and make it sql injection safe
def get_sum_of_meals_by_id(uid):
    """
This function takes a UID as input and returns the total cost of all meals consumed by the specified user.

Args:
    uid (str): The UID to search for in the database.
    
Returns:
    The total cost of all meals consumed by the specified user.
"""

    sql_statement = f"SELECT CT_VEG,CT_NORM, CT_VEG_KID, CT_NORM_KID, EPreis FROM PERSESS NATURAL JOIN ESS WHERE ID = {uid}"
    value = dbconnector.sql(sql_statement)
    value = json.loads(json.dumps(value))
    logging.debug(f"Preis pro Tag: {value}")
    summe = 0
    for i in range(0, len(value)):
        summe += value[i][0] * value[i][4]
        summe += value[i][1] * value[i][4]
        summe += value[i][2] * value[i][4] / 2
        summe += value[i][3] * value[i][4] / 2
        logging.debug(f"Zwischensumme: {summe}")
    return summe


def get_sum_of_all_by_id(uid):
    """Returns the sum of all GPREIS and EPREIS values for the given user id (uid)
    from the PERSGET, GETR, PERSESS, and ESS tables, joined by NATURAL JOIN.

    Args:
        uid: The user id to get the sum of GPREIS and EPREIS values for.

    Returns:
        The sum of GPREIS and EPREIS values for the given user id.
    """
    sql_statement = f"SELECT SUM(GPREIS) + SUM(EPREIS) FROM PERSGET NATURAL JOIN GETR NATURAL JOIN PERSESS NATURAL JOIN ESS WHERE ID = {uid}"
    return dbconnector.sql(sql_statement)


def get_all_edat_by_id(uid):
    """Returns all EDAT and CT values for the given user id (uid) from the PERSESS and ESS
    tables, joined by INNER JOIN. EDAT values are returned in the format "dd.mm.yyyy".

    Args:
        uid: The user id to get EDAT and CT values for.

    Returns:
        A list of EDAT and CT values for the given user id.
    """
    sql_statement = f'SELECT DATE_FORMAT(ESS.EDAT, "%d.%m.%Y"), PERSESS.CT_VEG, PERSESS.CT_NORM, PERSESS.CT_VEG_KID, PERSESS.CT_NORM_KID FROM PERSESS INNER JOIN Strichliste.ESS ON PERSESS.EID = ESS.EID WHERE ID = {uid};'
    return dbconnector.sql(sql_statement)


def get_vname_by_id(uid):
    """Returns the VNAME value for the given user id (uid) from the NAME table.

    Args:
        uid: The user id to get the VNAME value for.

    Returns:
        The VNAME value for the given user id.
    """
    sql_statement = f"SELECT VNAME FROM NAME WHERE ID = {uid}"
    vname = dbconnector.sql(sql_statement)
    vname = json.loads(json.dumps(vname))
    vname = vname[0][0]
    return vname


def get_nname_by_id(uid):
    """Returns the NNAME value for the given user id (uid) from the NAME table.

    Args:
        uid: The user id to get the NNAME value for.

    Returns:
        The NNAME value for the given user id.
    """
    sql_statement = f"SELECT NNAME FROM NAME WHERE ID = {uid}"
    nname = dbconnector.sql(sql_statement)
    nname = json.loads(json.dumps(nname))
    nname = nname[0][0]
    return nname


def get_stay_start_end_by_id(uid):
    """Returns the STAYDATE_START and STAYDATE_END values for the given user id (uid)
    from the STAY table.

    Args:
        uid: The user id to get STAYDATE_START and STAYDATE_END values for.

    Returns:
        A tuple containing the STAYDATE_START and STAYDATE_END values for the given
        user id.
    """
    sql_statement = f"SELECT STAYDATE_START, STAYDATE_END FROM STAY WHERE ID = {uid}"
    values = dbconnector.sql(sql_statement)
    try:
        startdate = values[0][0]
    except IndexError:
        startdate = 0
    try:
        enddate = values[0][1]
    except IndexError:
        enddate = 0
    logging.debug(f"Startdate: {startdate} Enddate: {enddate}")
    return startdate, enddate


def get_staycost_by_id(uid):
    """Returns the full cost of the user's stay, based on the CTR value in the STAY table
    for the given user id (uid) and the configured stay cost.

    Args:
        uid: The user id to get the stay cost for.

    Returns:
        The full cost of the user's stay.
    """
    sql_statement = f"SELECT CTR FROM STAY WHERE ID = {uid}"
    counter = dbconnector.sql(sql_statement)
    counter = json.loads(json.dumps(counter))
    try:
        counter = counter[0][0]
    except IndexError:
        counter = 0
    logging.debug(f"Staycounter: {counter}")
    cost = getConfig.get_config("stay_cost")
    logging.debug(f"Staycost: {cost}")
    fullcost = float(cost) * counter
    return fullcost


def get_stay_counter_by_id(uid):
    """Returns the CTR value for the given user id (uid) from the STAY table.

    Args:
        uid: The user id to get the CTR value for.

    Returns:
        The CTR value for the given user id.
    """
    sql_statement = f"SELECT CTR FROM STAY WHERE ID = {uid}"
    counter = dbconnector.sql(sql_statement)
    counter = json.loads(json.dumps(counter))
    try:
        counter = counter[0][0]
    except IndexError:
        counter = 0
    return counter


def set_stay_counter(uid, counter):
    """Sets the CTR value for the given user id (uid) in the STAY table to the
    given counter value.

    Args:
        uid: The user id to set the CTR value for.
        counter: The value to set the CTR to.
    """
    if not get_stay_counter_by_id(uid):
        sql_statement = f"INSERT INTO STAY VALUES ({uid}, NULL, NULL, {counter})"
        dbconnector.sql(sql_statement)
    sql_statement = f"UPDATE STAY SET CTR = {counter} WHERE ID = {uid}"
    dbconnector.sql(sql_statement)


def set_stay_start_end(uid, start, end):
    """Sets the STAYDATE_START and STAYDATE_END values for the given user id (uid)
    in the STAY table to the given start and end date values.

    Args:
        uid: The user id to set the STAYDATE_START and STAYDATE_END values for.
        start: The STAYDATE_START value to set.
        end: The STAYDATE_END value to set.
    """
    if not get_stay_start_end_by_id(uid):
        sql_statement = f"INSERT INTO STAY VALUES ({uid}, '{start}', '{end}', 0)"
        dbconnector.sql(sql_statement)
    sql_statement = f"UPDATE STAY SET STAYDATE_START = '{start}', STAYDATE_END = '{end}' WHERE ID = {uid}"
    dbconnector.sql(sql_statement)


def set_user_id_by_name(vname, nname):
    """Inserts a new user into the ID and NAME tables, based on the given VNAME and NNAME values.

    Args:
        vname: The VNAME value for the new user.
        nname: The NNAME value for the new user.

    Returns:
        The user id of the newly inserted user.
    """
    vfid = get_vfid_by_name_from_vf(vname, nname)
    logging.debug("got vfid: " + str(vfid))
    sql_statement = f"INSERT INTO ID VALUES (NULL, {vfid})"  ## Null is for auto increment of the ID
    dbconnector.sql(sql_statement)
    sql_statement = "SELECT MAX(ID) FROM ID "
    uid = dbconnector.sql(sql_statement)
    int_id = int(json.loads(json.dumps(uid))[0][0])
    logging.debug(f"got ID: {int_id}")
    sql_statement = f"INSERT INTO NAME VALUES ({int_id},'{vname}','{nname}')"
    dbconnector.sql(sql_statement)
    return uid


def set_eid_with_date():
    """
        This function inserts a new event into the 'ESS' table in the database with a new EID, the current date, and the meal cost.

        The new EID is calculated by finding the maximum EID currently in the 'ESS' table and adding 1 to it. The meal cost is retrieved from the configuration.

        The function does not take any arguments and does not return any value. It directly interacts with the database to perform the insertion operation.
        """
    sql_statement = "SELECT MAX(EID) FROM ESS "
    max_eid = dbconnector.sql(sql_statement)
    max_eid = int(json.loads(json.dumps(max_eid))[0][0]) + 1
    meal_cost = getConfig.get_config('meal_cost')
    date = datetime.date.today().strftime("%Y-%m-%d")
    sql_statement = f"INSERT INTO ESS VALUES ({max_eid}, {meal_cost}, '{date}')"  ## Null is for auto increment of the ID
    dbconnector.sql(sql_statement)


def set_drink_ct_by_id_and_uid(beer, water, icetea, softdrinks, uid):
    """
        This function updates the count of each type of drink for a specific user in the 'PERSGET' table in the database.

        The function takes the count of each type of drink and the user ID as inputs. It then tries to update the count of each type of drink for the user in the 'PERSGET' table. If the user does not exist in the table, it inserts a new row with the user ID and the counts of each type of drink.

        Args:
            beer (int): The count of beers.
            water (int): The count of waters.
            icetea (int): The count of iceteas.
            softdrinks (int): The count of softdrinks.
            uid (int): The user ID.

        Raises:
            IndexError: If the user does not exist in the 'PERSGET' table, the function will insert a new row with the user ID and the counts of each type of drink.
        """
    logging.debug(f"got drinklist: beer:{beer}, water:{water} icetea:{icetea} softdrinks:{softdrinks} uid: {uid}")
    getraenke = [water, beer, softdrinks, icetea]
    for i in range(4):
        try:
            sql_statement = f"UPDATE `PERSGET` SET CT ='{getraenke[i]}' WHERE ID = '{uid}' AND GID = '{i + 1}' "
            dbconnector.sql(sql_statement)
        except IndexError:
            logging.debug("Error while inserting into PERSGET table. Data does not exists. Inserting...")
            sql_statement = f"INSERT INTO `PERSGET` VALUES ({uid},{i + 1},{getraenke[i]})"
            dbconnector.sql(sql_statement)


def set_meal_ct_by_id_and_uid(veg, norm, veg_kid, norm_kid, uid):
    """
       This function updates the count of each type of meal for a specific user in the 'PERSESS' table in the database.

       The function takes the count of each type of meal and the user ID as inputs. It then tries to update the count of each type of meal for the user in the 'PERSESS' table. If the user does not exist in the table, it inserts a new row with the user ID and the counts of each type of meal.

       Args:
           veg (int): The count of vegetarian meals.
           norm (int): The count of normal meals.
           veg_kid (int): The count of vegetarian meals for kids.
           norm_kid (int): The count of normal meals for kids.
           uid (int): The user ID.

       Raises:
           IndexError: If the user does not exist in the 'PERSESS' table, the function will insert a new row with the user ID and the counts of each type of meal.
       """
    logging.debug(
        f"got meal: vegetarian:{veg}, normal:{norm} vegetarian_kid:{veg_kid} normal_kid:{norm_kid} uid: {uid}")
    meals = [veg, norm, veg_kid, norm_kid]
    eid = get_eid_by_date(datetime.date.today().strftime("%Y-%m-%d"))
    eid = json.loads(json.dumps(eid))[0][0]
    if not get_persess_by_id_and_eid(uid, eid):
        sql_statement = f"INSERT INTO `PERSESS` VALUES ({uid},{eid},{meals[0]},{meals[1]},{meals[2]},{meals[3]})"
        dbconnector.sql(sql_statement)
    else:
        logging.debug("Error while inserting into PERSESS table. Data already exists. Updating...")
        sql_statement = f"UPDATE `PERSESS` SET CT_NORM ='{meals[0]}' WHERE ID = '{uid}' AND EID = '{eid}'"
        dbconnector.sql(sql_statement)
        sql_statement = f"UPDATE `PERSESS` SET CT_VEG ='{meals[1]}' WHERE ID = '{uid}' AND EID = '{eid}'"
        dbconnector.sql(sql_statement)
        sql_statement = f"UPDATE `PERSESS` SET CT_NORM_KID ='{meals[2]}' WHERE ID = '{uid}' AND EID = '{eid}'"
        dbconnector.sql(sql_statement)
        sql_statement = f"UPDATE `PERSESS` SET CT_VEG_KID ='{meals[3]}' WHERE ID = '{uid}' AND EID = '{eid}'"
        dbconnector.sql(sql_statement)


def close_meal_today():
    """
    This function closes the meal for today by setting the EID of the user to 0 in the 'PERSESS' table in the database.

    The function does not take any arguments and does not return any value. It directly interacts with the database to perform the update operation.
    """
    date = datetime.date.today()
    tomorrow = date + datetime.timedelta(days=1)
    tomorrow = tomorrow.strftime("%Y-%m-%d")
    date = date.strftime("%Y-%m-%d")
    eid = get_eid_by_date(date)
    eid = int(json.loads(json.dumps(eid))[0][0])
    sql_statement = f"INSERT INTO `ESS` (EID, EDAT, is_latest) VALUES ({eid + 1},{tomorrow}, TRUE)"
    dbconnector.sql(sql_statement)
    logging.debug("Closed meal for today")

def get_meal_date():
    """
    This function returns the date of the meal for today.

    The function does not take any arguments and returns the date of the meal for today.
    """

    sql_statement = f"SELECT EDAT FROM ESS WHERE isLatest = TRUE"
    date = dbconnector.sql(sql_statement)
    date = json.loads(json.dumps(date)[0][0])