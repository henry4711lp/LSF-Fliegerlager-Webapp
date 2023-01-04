import json
import logging
from datetime import date
from html import escape
from flask import Flask, render_template, request, redirect, url_for, make_response
from werkzeug.security import generate_password_hash, check_password_hash
from flask_httpauth import HTTPBasicAuth

import dbconnector
import dbdata
import getConfig
import webwork
import dbexport

# create flask app
app = Flask(__name__, static_url_path='/static')
UserID = 0
httpAuth = HTTPBasicAuth()
user = getConfig.get_config("admin_username")
pw = getConfig.get_config("admin_password")
users = {
    user: generate_password_hash(pw)
}


@httpAuth.verify_password
def verify_password(username, password):
    if username in users:
        return check_password_hash(users.get(username), password)
    return False


@app.route('/export')
@httpAuth.login_required
def export():
    return dbexport.export()


@app.route('/')
def index():
    return redirect(url_for('register'))


@app.route('/register')
def register():
    resp = make_response(render_template("register.html"))
    resp.set_cookie("UserID", '0', max_age=0)
    return resp


@app.route("/home", methods=["POST", "GET"])  # TODO: Display VName in HTML
def home():
    if request.method == "POST":
        if '/register' in request.referrer:
            logging.debug("Post from login")
            return webwork.signup_in(request)
        elif '/stays' in request.referrer:
            logging.debug("Post from stays")
            return webwork.stay(request)
        elif '/drinkselector' in request.referrer:
            logging.debug("Post from drinkselector")
            return webwork.drink(request)
        elif '/mealselector' in request.referrer:
            logging.debug("Post from mealselector")
            return webwork.meal(request)
    print(request)
    return webwork.empty()


@app.route("/stays")
def stays():
    uid = get_uid_from_cookie()
    vname = dbdata.get_vname_by_id(uid)
    nname = dbdata.get_nname_by_id(uid)
    counter = dbdata.get_stay_counter_by_id(uid)
    start, end = dbdata.get_stay_start_end_by_id(uid)
    return render_template("stays.html", counter=counter, vname=vname, nname=nname, start=start, end=end)


@app.route("/bill")
def bill():
    return webwork.billing()


@app.route("/get-cookies/UserID")
def get_uid_from_cookie():
    logging.debug("UserID: " + request.cookies.get("UserID"))
    cookie = request.cookies.get("UserID")
    return escape(cookie)  # returns the UserID cookie


@app.route("/get-Vname-by-ID")
def get_vname_by_id():
    ID = request.cookies.get("UserID")
    sql_statement = f"SELECT VNAME FROM NAME WHERE ID = {ID}"
    logging.debug(json.dumps(dbconnector.sql(sql_statement)))
    return str(json.dumps(dbconnector.sql(sql_statement)))


@app.route("/drinkselector")  # TODO: Make it possible to send the data to the database
def drinkselector():
    uid = request.cookies.get("UserID")
    water_price = dbdata.get_gprice_by_id(1)
    water_ct = dbdata.get_persget_by_id_and_gid(uid, 1)
    beer_price = dbdata.get_gprice_by_id(2)
    beer_ct = dbdata.get_persget_by_id_and_gid(uid, 2)
    soft_price = dbdata.get_gprice_by_id(3)
    soft_ct = dbdata.get_persget_by_id_and_gid(uid, 3)
    icetea_price = dbdata.get_gprice_by_id(4)
    icetea_ct = dbdata.get_persget_by_id_and_gid(uid, 4)
    print(f"{beer_ct}")
    return render_template("drinkselector.html", beer_price=beer_price, water_price=water_price,
                           icetea_price=icetea_price, soft_price=soft_price, beer_ct=beer_ct, water_ct=water_ct,
                           icetea_ct=icetea_ct, soft_ct=soft_ct)


@app.route("/mealselector")
def mealselector():
    mealdate = date.today().strftime("%d.%m.%Y")
    return render_template("mealselector.html", mealdate=mealdate)


@app.route("/dbtest")
def dbtest():
    sql_statement = f"SELECT MAX(ID) FROM ID "
    return dbconnector.sql(sql_statement)


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
