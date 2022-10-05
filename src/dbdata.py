import json
import logging

from src.connection import dbconnector, vf_data

logging.basicConfig(level=logging.DEBUG)
def get_id_by_name(vname, nname):
    sql_statement = "SELECT ID FROM NAME WHERE VNAME = '" + vname + "' AND NNAME = '" + nname + "'"
    return dbconnector.sql(sql_statement)


def get_vfid_by_name_from_VF(vname, nname):
    return vf_data.get_vfid(vname, nname)


def get_EID_by_date(date):
    sql_statement = "SELECT EID FROM ESS WHERE EDAT = '" + date + "'"
    return dbconnector.sql(sql_statement)


def get_GPreis_by_GID(gid):
    sql_statement = "SELECT GPREIS FROM GETR WHERE GID = '" + gid + "'"
    return dbconnector.sql(sql_statement)


def get_PERSESS_by_ID_and_EID(pid, eid):
    sql_statement = "SELECT * FROM PERSESS WHERE ID = '" + pid + "' AND EID = '" + eid + "'"
    return dbconnector.sql(sql_statement)


def get_PERSGET_by_ID_and_GID(pid, gid):
    sql_statement = "SELECT * FROM PERSGET WHERE ID = '" + pid + "' AND GID = '" + gid + "'"
    return dbconnector.sql(sql_statement)


def set_user_id_by_name(vname, nname):
    vfid = get_vfid_by_name_from_VF(vname, nname)
    logging.info("got vfid: " + str(vfid))
    sql_statement = f"INSERT INTO ID VALUES (NULL, {vfid})" ## Null is for auto increment of the ID
    dbconnector.sql(sql_statement)
    sql_statement = "SELECT MAX(ID) FROM ID "
    ID = dbconnector.sql(sql_statement)
    intID = int(json.loads(json.dumps(ID))[0][0])
    intID = intID
    logging.info(f"got ID: {intID}")
    sql_statement = f"INSERT INTO NAME VALUES ({intID},'{vname}','{nname}')"
    dbconnector.sql(sql_statement)
    return ID

