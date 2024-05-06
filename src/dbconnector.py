import logging
import mysql.connector
from mysqlx.helpers import escape

import getConfig


logging.basicConfig(level=logging.DEBUG)


def sql(sql_statement):
    """
    Connects to a database using the `mysql.connector` library, using a user and password defined in the `config.yaml`
    file. The connection parameters are retrieved from the `config.yaml` file using the `getConfig.py` file.
    
    Executes the given `sql_statement` on the connected database, and returns all rows of the result.
    
    :param sql_statement: The SQL statement to be executed on the database.
    :type sql_statement: str
    :return: All rows of the result of the executed SQL statement.
    :rtype: List[Tuple[Any]]
    """
    # gets the config from the config.yaml file via the get_config.py file
    cnx = mysql.connector.connect(user=getConfig.get_config("db_user"), password=getConfig.get_config("db_password"),
                                  host=getConfig.get_config("db_host"), database=getConfig.get_config("db_name"),
                                  port=getConfig.get_config("db_port"),
                                  ssl_disabled=getConfig.get_config("db_ssl_disabled"))
    if cnx.is_connected():
        logging.debug("Connected to database")
        cursor = cnx.cursor()  # create cursor
        cursor.execute(sql_statement)  # execute the given sql statement
        logging.debug(f"Executed sql statement {sql_statement}")
        rows = cursor.fetchall()  # fetches all rows
        cnx.commit()  # commit changes
        cursor.close()  # close cursor
        cnx.close()  # close connection
        logging.debug("Closed connection to database")
    else:
        logging.error("Connection to database failed")
        rows = 0
    return rows  # returns all rows
