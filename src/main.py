import json
import logging
import datetime
from html import escape
from flask import Flask, render_template, request, redirect, url_for, make_response
from werkzeug.security import generate_password_hash, check_password_hash
from flask_httpauth import HTTPBasicAuth

from apscheduler.schedulers.background import BackgroundScheduler

import dbconnector
import dbdata
import getConfig
import webwork
import dbexport
import vf_data
# create flask app
app = Flask(__name__, static_url_path='/static')
UserID = 0
httpAuth = HTTPBasicAuth()
user = getConfig.get_config("admin_username")
pw = getConfig.get_config("admin_password")
users = {
    user: generate_password_hash(pw)
}


@app.route('/test')
def test():
    vf_id = vf_data.get_vfid("jan", "sellerbeck")
    uid = get_uid_from_cookie()
    vf_id= vf_data.get_starts_by_date_and_id("2024-05-01", uid)
    resp = make_response(str(vf_id))
    return resp


@httpAuth.verify_password
def verify_password(username, password):
    if username in users:
        return check_password_hash(users.get(username), password)
    return False


@app.route('/export')
@httpAuth.login_required
def export():
    return dbexport.export()


@app.route('/shutdown')
@httpAuth.login_required
def shutdown():
    logging.info("Shutdown called")
    quit(0)


@app.route('/')
def index():
    return redirect(url_for('register'))


@app.route('/register')
def register():
    resp = make_response(render_template("register.html"))
    resp.set_cookie("UserID", '0', max_age=0)
    return resp


@app.route("/home", methods=["POST", "GET"])
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
    return webwork.empty()


@app.route("/stays")
def stays():
    try:
        uid = get_uid_from_cookie()
    except TypeError:
        return redirect(url_for('register'))
    vname = dbdata.get_vname_by_id(uid)
    nname = dbdata.get_nname_by_id(uid)
    counter = dbdata.get_stay_counter_by_id(uid)
    start, end = dbdata.get_stay_start_end_by_id(uid)
    return render_template("stays.html", counter=counter, vname=vname, nname=nname, start=start, end=end)


@app.route("/bill")
def bill():
    try:
        return webwork.billing()
    except TypeError:
        return redirect(url_for('register'))


@app.route("/get-cookies/UserID")
def get_uid_from_cookie():
    logging.debug("UserID: " + request.cookies.get("UserID"))
    cookie = request.cookies.get("UserID")
    return escape(cookie)  # returns the UserID cookie


@app.route("/get-Vname-by-ID")
def get_vname_by_id():
    uid = request.cookies.get("UserID")
    uid = escape(uid)
    sql_statement = f"SELECT VNAME FROM NAME WHERE ID = {uid}"
    logging.debug(json.dumps(dbconnector.sql(sql_statement)))
    return str(json.dumps(dbconnector.sql(sql_statement)))


@app.route("/drinkselector")
def drinkselector():
    uid = request.cookies.get("UserID")
    water_price = dbdata.get_gprice_by_id(str(1))
    #try:
    water_ct = dbdata.get_persget_by_id_and_gid(uid, str(1))
    #except IndexError:
        #return redirect(url_for('register'))
    beer_price = dbdata.get_gprice_by_id(str(2))
    beer_ct = dbdata.get_persget_by_id_and_gid(uid, str(2))
    soft_price = dbdata.get_gprice_by_id(str(3))
    soft_ct = dbdata.get_persget_by_id_and_gid(uid, str(3))
    icetea_price = dbdata.get_gprice_by_id(str(4))
    icetea_ct = dbdata.get_persget_by_id_and_gid(uid, str(4))
    return render_template("drinkselector.html", beer_price=beer_price, water_price=water_price,
                           icetea_price=icetea_price, soft_price=soft_price, beer_ct=beer_ct, water_ct=water_ct,
                           icetea_ct=icetea_ct, soft_ct=soft_ct)


@app.route("/mealselector")
def mealselector():
    uid = request.cookies.get("UserID")
    date = datetime.date.today().strftime("%Y-%m-%d")
    eid = dbdata.get_eid_by_date(date)
    eid = eid[0][0]
    try:
        cts = dbdata.get_persess_by_id_and_eid(uid, eid)
    except TypeError:
        return redirect(url_for('register'))
    try:
        vegetarian_ct = cts[0][2]
        normal_ct = cts[0][3]
        kid_vegetarian_ct = cts[0][4]
        kid_normal_ct = cts[0][5]
    except IndexError:
        normal_ct = 0
        vegetarian_ct = 0
        kid_normal_ct = 0
        kid_vegetarian_ct = 0
    prices = getConfig.get_config("meal_cost")
    prices = float(prices)
    kid_price = prices/2
    prices = "" + str(prices) + "0 €"
    kid_price = "" + str(kid_price) + " €"
    mealdate = datetime.date.today().strftime("%d.%m.%Y")
    return render_template("mealselector.html", mealdate=mealdate, normal_price=prices, vegetarian_price=prices,
                           kid_normal_price=kid_price, kid_vegetarian_price=kid_price, normal_ct=normal_ct, vegetarian_ct=vegetarian_ct,
                           kid_normal_ct=kid_normal_ct, kid_vegetarian_ct=kid_vegetarian_ct)




@app.route("/dbtest")
def dbtest():
    sql_statement = f"SELECT MAX(ID) FROM ID "
    return dbconnector.sql(sql_statement)


if __name__ == '__main__':
    sched = BackgroundScheduler(daemon=True)
    sched.add_job(dbexport.export, 'interval', minutes=60)
    sched.start()
    logging.basicConfig(level=logging.DEBUG)
    app.run(debug=True, host="0.0.0.0")
