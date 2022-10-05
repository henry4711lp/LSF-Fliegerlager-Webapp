import json
import logging

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
