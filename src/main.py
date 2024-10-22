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
#users = {
#    user: generate_password_hash(pw)
#}


@app.route('/test')
def test():
    vf_id = vf_data.get_vfid("jan", "sellerbeck")
    uid = get_uid_from_cookie()
    vf_id = vf_data.get_starts_by_date_and_id("2024-05-01", uid)
    resp = make_response(str(vf_id))
    return resp


@httpAuth.verify_password
@app.route('/close_meal_today')
def close_meal_today():
    dbdata.close_meal_today()
    return "Success"

@app.route('/get_meal_today')
def get_meal_today():
    return dbdata.get_meal_date()
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
        referrer_endpoints = ['/register', '/stays', '/drinkselector', '/mealselector']
        functions = [webwork.signup_in, webwork.stay, webwork.drink, webwork.meal]
        for endpoint, function in zip(referrer_endpoints, functions):
            if endpoint in request.referrer:
                logging.debug(f"Post from {endpoint[1:]}")
                return function(request)
    return webwork.empty()


@app.route("/stays")
def stays():
    uid = request.cookies.get("UserID")
    if uid is None:
        return redirect(url_for('register'))
    vname, nname, counter = dbdata.get_vname_by_id(uid), dbdata.get_nname_by_id(uid), dbdata.get_stay_counter_by_id(uid)
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
    uid = request.cookies.get("UserID")
    if uid is None:
        return redirect(url_for('register'))
    return escape(uid)


@app.route("/get-Vname-by-ID")
def get_vname_by_id():
    uid = request.cookies.get("UserID")
    uid = escape(uid)
    sql_statement = f"SELECT VNAME FROM NAME WHERE ID = {uid}"
    logging.debug(json.dumps(dbconnector.sql(sql_statement)))
    return str(json.dumps(dbconnector.sql(sql_statement)))


@app.route("/drinkselector")
def drinkselector():
    """
        This is a Flask route that handles requests to the "/drinkselector" endpoint.

        When a GET request is made to this endpoint, it retrieves the user ID from the cookies.
        If the user ID is not found, it redirects to the 'register' page.

        It then creates a list of drinks and retrieves the prices and counts for each drink from the database.
        The prices and counts are then passed to the "drinkselector.html" template and rendered.

        Returns:
            str: A string of HTML rendered with the "drinkselector.html" template.
        """
    uid = request.cookies.get("UserID")
    if uid is None:
        return redirect(url_for('register'))
    drinks = ['water', 'beer', 'soft', 'icetea']
    prices = {drink: dbdata.get_gprice_by_id(str(i + 1)) for i, drink in enumerate(drinks)}
    counts = {drink: dbdata.get_persget_by_id_and_gid(uid, str(i + 1)) for i, drink in enumerate(drinks)}
    return render_template("drinkselector.html", beer_price=prices['beer'], water_price=prices['water'],
                           icetea_price=prices['icetea'], soft_price=prices['soft'], beer_ct=counts['beer'],
                           water_ct=counts['water'], icetea_ct=counts['icetea'], soft_ct=counts['soft'])


@app.route("/mealselector")
def mealselector():
    """
      This is a Flask route that handles requests to the "/mealselector" endpoint.

      When a GET request is made to this endpoint, it retrieves the user ID from the cookies.
      If the user ID is not found, it redirects to the 'register' page.

      It then retrieves the event ID corresponding to today's date and the meal counts for the user.
      If the meal counts are not found, it redirects to the 'register' page.

      The meal counts are then used to calculate the prices for different types of meals.
      The prices and meal counts are then passed to the "mealselector.html" template and rendered.

      Returns:
          render_template: Returns the "mealselector.html" template filled with the according data.
      """
    uid = request.cookies.get("UserID")
    if uid is None:
        return redirect(url_for('register'))
    date = datetime.date.today().strftime("%Y-%m-%d")
    eid = dbdata.get_eid_by_date(date)
    eid = eid[0][0]
    cts = dbdata.get_persess_by_id_and_eid(uid, eid)
    meal_counts = cts[0][2:6]
    meal_counts = [count or 0 for count in meal_counts]
    vegetarian_ct, normal_ct, kid_vegetarian_ct, kid_normal_ct = meal_counts
    prices = float(getConfig.get_config("meal_cost"))
    kid_price = prices / 2
    prices = f"{prices}0 €"
    kid_price = f"{kid_price} €"
    mealdate = datetime.date.today().strftime("%d.%m.%Y")
    return render_template("mealselector.html", mealdate=mealdate, normal_price=prices, vegetarian_price=prices,
                           kid_normal_price=kid_price, kid_vegetarian_price=kid_price, normal_ct=normal_ct,
                           vegetarian_ct=vegetarian_ct,
                           kid_normal_ct=kid_normal_ct, kid_vegetarian_ct=kid_vegetarian_ct)


@app.route("/dbtest")
def dbtest():
    """
    This is a Flask route that handles requests to the "/dbtest" endpoint.

    When a GET request is made to this endpoint, it executes a SQL query to
    retrieve the maximum ID from the ID table in the database. The result of
    this query is then returned as the response to the request.

    Returns:
        list: A list containing the result of the SQL query. If the query is
        successful, the list will contain a single element which is the maximum
        ID. If the query fails, the list will be empty.
    """
    sql_statement = f"SELECT MAX(ID) FROM ID "
    return dbconnector.sql(sql_statement)


if __name__ == '__main__':
    sched = BackgroundScheduler(daemon=True)
    sched.add_job(dbexport.export, 'interval', minutes=60)
    sched.start()
    logging.basicConfig(level=logging.DEBUG)
    app.run(debug=True, host="0.0.0.0", port=getConfig.get_config("application_port"))
