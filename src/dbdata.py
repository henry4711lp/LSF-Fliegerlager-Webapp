import json
import logging

from src import formatprices, getConfig
from src.connection import dbconnector, vf_data

logging.basicConfig(level=logging.DEBUG)


def get_id_by_name(vname, nname):
    sql_statement = "SELECT ID FROM NAME WHERE VNAME = '" + vname + "' AND NNAME = '" + nname + "'"
    return dbconnector.sql(sql_statement)


def get_vfid_by_name_from_vf(vname, nname):
    return vf_data.get_vfid(vname, nname)


def get_eid_by_date(date):
    sql_statement = "SELECT EID FROM ESS WHERE EDAT = '" + date + "'"
    return dbconnector.sql(sql_statement)


def get_gpreis_by_gid(gid):
    sql_statement = "SELECT GPREIS FROM GETR WHERE GID = '" + gid + "'"
    return dbconnector.sql(sql_statement)


def get_all_gpreis():
    sql_statement = f"SELECT GPREIS FROM GETR;"
    return dbconnector.sql(sql_statement)


def get_persess_by_id_and_eid(pid, eid):
    sql_statement = "SELECT * FROM PERSESS WHERE ID = '" + pid + "' AND EID = '" + eid + "'"
    return dbconnector.sql(sql_statement)


def get_persget_by_id_and_gid(pid, gid):
    sql_statement = "SELECT * FROM PERSGET WHERE ID = '" + pid + "' AND GID = '" + gid + "'"
    return dbconnector.sql(sql_statement)


def set_user_id_by_name(vname, nname):
    vfid = get_vfid_by_name_from_vf(vname, nname)
    logging.info("got vfid: " + str(vfid))
    sql_statement = f"INSERT INTO ID VALUES (NULL, {vfid})"  ## Null is for auto increment of the ID
    dbconnector.sql(sql_statement)
    sql_statement = "SELECT MAX(ID) FROM ID "
    uid = dbconnector.sql(sql_statement)
    int_id = int(json.loads(json.dumps(uid))[0][0])
    logging.info(f"got ID: {int_id}")
    sql_statement = f"INSERT INTO NAME VALUES ({int_id},'{vname}','{nname}')"
    dbconnector.sql(sql_statement)
    return uid


def get_sum_of_drink_by_id_and_gid(uid, gid):
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
    sql_statement = f"SELECT CT*EPREIS FROM PERSESS NATURAL JOIN ESS WHERE ID = {uid}"
    value = dbconnector.sql(sql_statement)
    value = json.loads(json.dumps(value))
    logging.debug(f"Preis pro Tag: {value}")
    summe = 0
    for i in range(0, len(value)):
        summe += value[i][0]
        logging.debug(f"Zwischensumme: {summe}")
    return summe


def get_sum_of_all_by_id(uid):
    sql_statement = f"SELECT SUM(GPREIS) + SUM(EPREIS) FROM PERSGET NATURAL JOIN GETR NATURAL JOIN PERSESS NATURAL JOIN ESS WHERE ID = {uid}"
    return dbconnector.sql(sql_statement)


def get_all_edat_by_id(uid):
    sql_statement = f'SELECT DATE_FORMAT(ESS.EDAT, "%d.%m.%Y"), PERSESS.CT FROM PERSESS INNER JOIN Strichliste.ESS ON PERSESS.EID = ESS.EID WHERE ID = {uid};'
    return dbconnector.sql(sql_statement)


def get_vname_by_id(uid):
    sql_statement = f"SELECT VNAME FROM NAME WHERE ID = {uid}"
    vname = dbconnector.sql(sql_statement)
    vname = json.loads(json.dumps(vname))
    vname = vname[0][0]
    return vname


def get_nname_by_id(uid):
    sql_statement = f"SELECT NNAME FROM NAME WHERE ID = {uid}"
    nname = dbconnector.sql(sql_statement)
    nname = json.loads(json.dumps(nname))
    nname = nname[0][0]
    return nname


def get_stay_start_end_by_id(uid):
    sql_statement = f"SELECT STAYDATE_START, STAYDATE_END FROM STAY WHERE ID = {uid}"
    return dbconnector.sql(sql_statement)


def get_staycost_by_id(uid):
    sql_statement = f"SELECT CTR FROM STAY WHERE ID = {uid}"
    counter = dbconnector.sql(sql_statement)
    counter = json.loads(json.dumps(counter))
    counter = counter[0][0]
    logging.debug(f"Staycounter: {counter}")
    cost = getConfig.get_config("stay_cost")
    logging.debug(f"Staycost: {cost}")
    fullcost = cost * counter
    return fullcost
