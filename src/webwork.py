import datetime
import json
import logging
from datetime import date
from html import escape

from flask import make_response, render_template, redirect, url_for
import dbdata
import formatprices
import main
import tablegenerator


def signup_in(request):
    vname = request.form["vname"]
    vname = escape(vname)
    nname = request.form["nname"]
    nname = escape(nname)
    uid = json.dumps(dbdata.get_id_by_name(vname, nname))
    logging.debug("uid: " + str(uid))
    if uid == "[]":
        # add new user to database
        dbdata.set_user_id_by_name(vname, nname)
    else:
        logging.info("User already exists with uid: " + str(uid))
    uid = dbdata.get_id_by_name(vname, nname)
    uid = int(json.loads(json.dumps(uid))[0][0])

    today = date.today().strftime("%d.%m.%Y")
    str_uid = str(uid)

    resp = make_response(render_template("home.html", ID=uid, date=today, display_name=vname, display_ID=str_uid))
    if logging.getLogger().getEffectiveLevel() == logging.DEBUG:
        logging.debug("UserID: " + request.cookies.get("UserID"))
        resp.set_cookie("UserID", f'{uid}')
    else:
        resp.set_cookie("UserID", f'{uid}', max_age=320)
    # Man könnte hier noch eine Ablaufzeit für die Cookies setzen mit resp.set_cookie(
    # "UserID", f'{uid}', max_age=<ExpirationTime>))
    return resp


def stay(request):
    uid = main.get_uid_from_cookie()

    # time calculation

    start = request.form["arrival"]
    start = datetime.datetime.strptime(start, "%Y-%m-%d")
    end = request.form["departure"]
    end = datetime.datetime.strptime(end, "%Y-%m-%d")
    delta = (end - start).days

    # database updates

    dbdata.set_stay_start_end(uid, start, end)
    dbdata.set_stay_counter(uid, delta)

    # necessary data for home.html#

    vname = dbdata.get_vname_by_id(uid)
    today = date.today().strftime("%d.%m.%Y")
    str_uid = str(uid)
    logging.debug(f"Start: {start}, End: {end} written to database generating response...")
    resp = make_response(render_template("home.html", ID=uid, date=today, display_name=vname, display_ID=str_uid))
    return resp


def drink(request):
    request = request.json
    uid = main.get_uid_from_cookie()
    dbdata.set_drink_ct_by_id_and_uid(request["beer"], request["water"], request["icetea"], request["softdrinks"], uid)
    vname = dbdata.get_vname_by_id(uid)
    today = date.today().strftime("%d.%m.%Y")
    str_uid = str(uid)
    resp = make_response(render_template("home.html", ID=uid, date=today, display_name=vname, display_ID=str_uid))
    return resp


def empty():
    try:
        uid = main.get_uid_from_cookie()
    except TypeError:
        return redirect(url_for('register'))
    vname = dbdata.get_vname_by_id(uid)
    today = date.today().strftime("%d.%m.%Y")
    str_uid = str(uid)
    resp = make_response(render_template("home.html", ID=uid, date=today, display_name=vname, display_ID=str_uid))
    return resp


def meal(request):
    request = request.json
    uid = main.get_uid_from_cookie()
    dbdata.set_meal_ct_by_id_and_uid(request["normal_ct"], request["vegetarian_ct"], request["kid_normal_ct"], request["kid_vegetarian_ct"], uid)
    vname = dbdata.get_vname_by_id(uid)
    today = date.today().strftime("%d.%m.%Y")
    str_uid = str(uid)
    resp = make_response(render_template("home.html", ID=uid, date=today, display_name=vname, display_ID=str_uid))
    return resp


def billing():
    uid = main.get_uid_from_cookie()
    nname = dbdata.get_nname_by_id(uid)
    vname = dbdata.get_vname_by_id(uid)
    sumbeer = dbdata.get_sum_of_drink_by_id_and_gid(uid, str(1))
    sumwater = dbdata.get_sum_of_drink_by_id_and_gid(uid, str(2))
    sumeistee = dbdata.get_sum_of_drink_by_id_and_gid(uid, str(3))
    sumsoft = dbdata.get_sum_of_drink_by_id_and_gid(uid, str(4))
    sumdrinks = formatprices.format_prices(dbdata.get_sum_of_drinks_by_id(uid))
    summeals = formatprices.format_prices(dbdata.get_sum_of_meals_by_id(uid))
    table = tablegenerator.get_table_food(dbdata.get_all_edat_by_id(uid))
    staycost = formatprices.format_prices(dbdata.get_staycost_by_id(uid))
    try:
        startdate = dbdata.get_stay_start_end_by_id(uid)[0].strftime("%d.%m.%Y")
    except AttributeError:
        startdate = datetime.datetime.today().strftime("%d.%m.%Y")
        logging.info("No startdate found")
    try:
        enddate = dbdata.get_stay_start_end_by_id(uid)[1].strftime("%d.%m.%Y")
    except AttributeError:
        enddate = datetime.datetime.today().strftime("%d.%m.%Y")
        logging.info("No enddate found")
    startstable = tablegenerator.get_table(dbdata.get_all_starts_by_date_and_id(uid, startdate, enddate))  # placeholder
    flycost = formatprices.format_prices(0)  # placeholder
    full_price = dbdata.get_sum_of_drinks_by_id(uid) + dbdata.get_sum_of_meals_by_id(uid) + dbdata.get_staycost_by_id(
        uid)
    full_price = formatprices.format_prices(full_price)

    return render_template("bill.html", nname=nname, vname=vname, sumbeer=sumbeer, sumwater=sumwater,
                           sumeistee=sumeistee, sumsoft=sumsoft, sum_drinks=sumdrinks, summeals=summeals,
                           full_price=full_price, staycost=staycost, startdate=startdate, enddate=enddate,
                           flycost=flycost, startstable=startstable, table=table)
