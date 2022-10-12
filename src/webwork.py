import json
import logging
from datetime import date

from flask import make_response, render_template

from src import dbdata


def signup_in(request):
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
