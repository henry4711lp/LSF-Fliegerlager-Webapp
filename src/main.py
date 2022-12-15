import hashlib
import hmac
import json
import logging
import os
import secrets
import threading
import time
from datetime import date
from flask import Flask, render_template, request, redirect, url_for, make_response
import dbconnector
import dbdata
import getConfig
import webwork

# create flask app
app = Flask(__name__, static_url_path='/static')
UserID = 0


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
    print(request)
    return render_template("error.html"), 404


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
    return request.cookies.get("UserID")  # returns the UserID cookie


@app.route("/get-Vname-by-ID")
def get_vname_by_id():
    ID = request.cookies.get("UserID")
    sql_statement = f"SELECT VNAME FROM NAME WHERE ID = {ID}"
    logging.debug(json.dumps(dbconnector.sql(sql_statement)))
    return str(json.dumps(dbconnector.sql(sql_statement)))


@app.route("/drinkselector")  # TODO: Make it possible to send the data to the database
def drinkselector():
    water_price = dbdata.get_gprice_by_id(1)
    beer_price = dbdata.get_gprice_by_id(2)
    soft_price = dbdata.get_gprice_by_id(3)
    icetea_price = dbdata.get_gprice_by_id(4)
    return render_template("drinkselector.html", beer_price=beer_price, water_price=water_price,
                           icetea_price=icetea_price, soft_price=soft_price)


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
