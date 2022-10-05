import json
import logging

from flask import Flask, render_template, request

from src import dbdata
from src.connection import dbconnector

# create flask app
app = Flask(__name__)


@app.route('/')
def index():
    return render_template("start.html")


@app.route('/register')
def register():
    return render_template("register.html")


@app.route("/home", methods=["POST", "GET"])
def home():
    if request.method == "POST":
        vname = request.form["vname"]
        nname = request.form["nname"]
        ID = json.dumps(dbdata.get_id_by_name(vname, nname))
        logging.debug("ID: " + str(ID))
        if ID == "[]":
            # add new user to database
            dbdata.set_user_id_by_name(vname, nname)
            ID = dbdata.get_id_by_name(vname, nname)
        else:
            logging.info("User already exists")
            logging.info(ID)
            return render_template("home.html", ID=ID)
    return render_template("home.html", ID=ID)


@app.route("/dbtest")
def dbtest():
        sql_statement = f"SELECT MAX(ID) FROM ID "
        return dbconnector.sql(sql_statement)


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
