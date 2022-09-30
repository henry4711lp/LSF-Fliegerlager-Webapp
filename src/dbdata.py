from src.connection import dbconnector, vf_data


def get_id_by_vname_and_nname(vname, nname):
    sql_statement = "SELECT ID FROM GETR WHERE VNAME = '" + vname + "' AND NNAME = '" + nname + "'"
    return dbconnector.sql(sql_statement)


def get_vfid_by_vname_and_nname_from_VF(vname, nname):
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