import json
import logging
from flask import Flask, render_template, request, make_response
from datetime import date
from src import dbdata
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
    return render_template("bill.html")

@app.route("/get-cookies/UserID")
def get_cookies_uid():
    return request.cookies.get("UserID")  # returns the UserID cookie


@app.route("/get-Vname-by-ID")
def get_vname_by_id():
    ID = request.cookies.get("UserID")
    sql_statement = f"SELECT VNAME FROM NAME WHERE ID = {ID}"
    print(json.dumps(dbconnector.sql(sql_statement)))
    return str(json.dumps(dbconnector.sql(sql_statement)))


@app.route("/drinkselector") #TODO: Display Prices in HTML
def drinkselector(): #TODO: Make HTML Buttons and counter work
    water_data = dbconnector.sql("SELECT GPreis from GETR WHERE GName = 'Wasser'")[0][0]
    water_price = '{:,.2f} €'.format(water_data).replace(".", ",")

    beer_data = dbconnector.sql("SELECT GPreis from GETR WHERE GName = 'Bier'")[0][0]
    beer_price = '{:,.2f} €'.format(beer_data).replace(".", ",")

    soft_data = dbconnector.sql("SELECT GPreis from GETR WHERE GName = 'Softdrink'")[0][0]
    soft_price = '{:,.2f} €'.format(soft_data).replace(".", ",")

    icetea_data = dbconnector.sql("SELECT GPreis from GETR WHERE GName = 'Eistee'")[0][0]
    icetea_price = '{:,.2f} €'.format(icetea_data).replace(".", ",")

    return render_template("drinkselector.html", beer_price=beer_price, water_price=water_price,
                           icetea_price=icetea_price, soft_price=soft_price)


@app.route("/dbtest")
def dbtest():
    sql_statement = f"SELECT MAX(ID) FROM ID "
    return dbconnector.sql(sql_statement)


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
