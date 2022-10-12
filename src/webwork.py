import datetime
import json
import logging
from datetime import date

from flask import make_response, render_template

from src import dbdata, formatprices, tablegenerator
from src.main import get_uid_from_cookie


def signup_in(request):
    vname = request.form["vname"]
    nname = request.form["nname"]
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
    resp.set_cookie("UserID", f'{uid}')
    # Man könnte hier noch eine Ablaufzeit für die Cookies setzen mit resp.set_cookie(
    # "UserID", f'{uid}', max_age=<ExpirationTime>))
    return resp


def stay(request): #TODO: redirect not working????
    uid = get_uid_from_cookie()

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


def billing():
    uid = get_uid_from_cookie()
    nname = dbdata.get_nname_by_id(uid)
    vname = dbdata.get_vname_by_id(uid)
    sumbeer = dbdata.get_sum_of_drink_by_id_and_gid(uid, 1)
    sumwater = dbdata.get_sum_of_drink_by_id_and_gid(uid, 2)
    sumeistee = dbdata.get_sum_of_drink_by_id_and_gid(uid, 3)
    sumsoft = dbdata.get_sum_of_drink_by_id_and_gid(uid, 4)
    sumdrinks = formatprices.format_prices(dbdata.get_sum_of_drinks_by_id(uid))
    summeals = formatprices.format_prices(dbdata.get_sum_of_meals_by_id(uid))
    table = tablegenerator.get_table(dbdata.get_all_edat_by_id(uid))
    full_price = dbdata.get_sum_of_drinks_by_id(uid) + dbdata.get_sum_of_meals_by_id(uid)
    full_price = formatprices.format_prices(full_price)
    staycost = formatprices.format_prices(dbdata.get_staycost_by_id(uid))
    startdate = dbdata.get_stay_start_end_by_id(uid)[0].strftime("%d.%m.%Y")
    enddate = dbdata.get_stay_start_end_by_id(uid)[1].strftime("%d.%m.%Y")
    flycost = formatprices.format_prices(0)  # placeholder

    return render_template("bill.html", nname=nname, vname=vname, sumbeer=sumbeer, sumwater=sumwater,
                           sumeistee=sumeistee, sumsoft=sumsoft, sum_drinks=sumdrinks, summeals=summeals,
                           full_price=full_price, staycost=staycost, startdate=startdate, enddate=enddate,
                           flycost=flycost, startstable=table, table=table)
