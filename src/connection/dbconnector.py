import logging

import mysql.connector
import src.getConfig as getConfig


logging.basicConfig(level=logging.DEBUG)


def sql(sql_statement):
    # gets the config from the config.yaml file via the get_config.py file
    cnx = mysql.connector.connect(user=getConfig.get_config("db_user"), password=getConfig.get_config("db_password"),
                                  host=getConfig.get_config("db_host"), database=getConfig.get_config("db_name"),
                                  port=getConfig.get_config("db_port"),
                                  ssl_disabled=getConfig.get_config("db_ssl_disabled"))
    if cnx.is_connected():
        logging.info("Connected to database")
        cursor = cnx.cursor()  # create cursor
        cursor.execute(sql_statement)  # execute the given sql statement
        logging.info(f"Executed sql statement {sql_statement}")
        rows = cursor.fetchall()  # fetches all rows
        cnx.commit()  # commit changes
        cursor.close()  # close cursor
        cnx.close()  # close connection
        logging.info("Closed connection to database")
    else:
        logging.error("Connection to database failed")
        rows = 0
    return rows  # returns all rows
