import http.client
import json
import logging

from flask import Flask, render_template, request, make_response, abort

from src import dbdata
from src.connection import dbconnector

# create flask app
app = Flask(__name__)
UserID = 0


@app.route('/')
def index():
    return render_template("start.html")


@app.route('/register')
def register():
    return render_template("register.html")


@app.route("/home", methods=["POST", "GET"])  # TODO: Display VName in HTML
def home():
    if request.method == "POST":
        vname = request.form["vname"]
        nname = request.form["nname"]
        ID = json.dumps(dbdata.get_id_by_name(vname, nname))
        logging.debug("ID: " + str(ID))
        if ID == "[]":
            # add new user to database
            dbdata.set_user_id_by_name(vname, nname)
        else:
            logging.info("User already exists")
            logging.info(ID)
        ID = dbdata.get_id_by_name(vname, nname)
        ID = int(json.loads(json.dumps(ID))[0][0])
        resp = make_response(render_template("home.html", ID=ID))
        resp.set_cookie("UserID", f'{ID}')
        # Man könnte hier noch eine Ablaufzeit für die Cookies setzen mit resp.set_cookie(
        # "UserID", f'{ID}', max_age=<ExpirationTime>))
        return resp


@app.route("/get-cookies/UserID")
def get_cookies_uid():
    return request.cookies.get("UserID")  # returns the UserID cookie


@app.route("/get-Vname-by-ID")
def get_vname_by_id():
    ID = request.cookies.get("UserID")
    sql_statement = f"SELECT VNAME FROM NAME WHERE ID = {ID}"
    print(json.dumps(dbconnector.sql(sql_statement)))
    return str(json.dumps(dbconnector.sql(sql_statement)))


@app.route("/dbtest")
def dbtest():
    sql_statement = f"SELECT MAX(ID) FROM ID "
    return dbconnector.sql(sql_statement)


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
