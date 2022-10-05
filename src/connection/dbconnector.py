import logging

import mysql.connector
from src import getConfig

logging.basicConfig(level=logging.DEBUG)


def sql(sql_statement):
    # gets the config from the config.yaml file via the getConfig.py file
    cnx = mysql.connector.connect(user=getConfig.getConfig("db_user"), password=getConfig.getConfig("db_password"),
                                  host=getConfig.getConfig("db_host"), database=getConfig.getConfig("db_name"),
                                  port=getConfig.getConfig("db_port"),
                                  ssl_disabled=getConfig.getConfig("db_ssl_disabled"))
    if cnx.is_connected():
        logging.INFO("Connected to database")
        cursor = cnx.cursor()  # create cursor
        cursor.execute(sql_statement)  # execute the given sql statement
        rows = cursor.fetchall()  # fetches all rows
        cursor.close()  # close cursor
        cnx.close()  # close connection
    else:
        logging.ERROR("Connection to database failed")
        rows = 0
    return rows  # returns all rows
