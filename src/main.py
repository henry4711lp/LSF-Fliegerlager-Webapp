import json
import logging
from flask import Flask, render_template, request, make_response
from datetime import date
from src import dbdata, tablegenerator, formatprices
from src.connection import dbconnector

# create flask app
app = Flask(__name__, static_url_path='/static')
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
            logging.info("User already exists with ID: " + str(ID))
        ID = dbdata.get_id_by_name(vname, nname)
        ID = int(json.loads(json.dumps(ID))[0][0])

        today = date.today().strftime("%d.%m.%Y")
        display_ID = str(ID)

        resp = make_response(render_template("home.html", ID=ID, date=today, display_name=vname, display_ID=display_ID))
        resp.set_cookie("UserID", f'{ID}')
        # Man könnte hier noch eine Ablaufzeit für die Cookies setzen mit resp.set_cookie(
        # "UserID", f'{ID}', max_age=<ExpirationTime>))
        return resp


@app.route("/bill")
def bill():
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
    staycost = formatprices.format_prices(0)  # placeholder
    startdate = date.fromisocalendar(2022, 23, 5).strftime("%d.%m.%Y")  # placeholder
    enddate = date.fromisocalendar(2022, 25, 3).strftime("%d.%m.%Y")  # placeholder
    flycost = formatprices.format_prices(0)  # placeholder
    return render_template("bill.html", nname=nname, vname=vname, sumbeer=sumbeer, sumwater=sumwater,
                           sumeistee=sumeistee, sumsoft=sumsoft, sum_drinks=sumdrinks, summeals=summeals,
                           full_price=full_price, staycost=staycost, startdate=startdate, enddate=enddate,
                           flycost=flycost, startstable=table, table=table)


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


@app.route("/drinkselector")  # TODO: Display Prices in HTML
def drinkselector():  # TODO: Make HTML Buttons and counter work
    water_data = dbconnector.sql("SELECT GPreis from GETR WHERE GName = 'Wasser'")[0][0]
    water_price = formatprices.format_prices(water_data)

    beer_data = dbconnector.sql("SELECT GPreis from GETR WHERE GName = 'Bier'")[0][0]
    beer_price = formatprices.format_prices(beer_data)

    soft_data = dbconnector.sql("SELECT GPreis from GETR WHERE GName = 'Softdrink'")[0][0]
    soft_price = formatprices.format_prices(soft_data)

    icetea_data = dbconnector.sql("SELECT GPreis from GETR WHERE GName = 'Eistee'")[0][0]
    icetea_price = formatprices.format_prices(icetea_data)

    return render_template("drinkselector.html", beer_price=beer_price, water_price=water_price,
                           icetea_price=icetea_price, soft_price=soft_price)


@app.route("/dbtest")
def dbtest():
    sql_statement = f"SELECT MAX(ID) FROM ID "
    return dbconnector.sql(sql_statement)


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
